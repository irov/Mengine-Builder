"""Resource-pack regression tests; native cases use the normal tool override."""
import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

from PIL import Image

from Builder.Build import build_resource_pack, configureBuilderActions
from Builder.Builder import Builder
from Builder.OSSystem import OSSystem
from Builder.PngOptimizer import PngOptimizer
from Builder.Project import Project
from Builder.Toolchain import required_tools_for_config


class PngPackFixture:
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source, self.destination = self.root / 'source', self.root / 'built'
        (self.source / 'Images').mkdir(parents=True)
        self.png = self.source / 'Images/icon.png'
        image = Image.new('RGBA', (4, 1))
        image.putdata([(255, 127, 63, alpha) for alpha in (0, 64, 128, 255)])
        image.save(self.png)
        self.original = self.png.read_bytes()
        self.package()

    def package(self, entries=None, format='xml'):
        entries = entries or [('Image', 'Images/icon.png', '0')]
        records = [{'Name': name, 'Type': 'ResourceImageDefault', 'Precompile': '0',
                    'File': {'Path': path, 'Premultiply': pma, 'Alpha': '1',
                             'MaxSize': '4 1', 'NoAtlas': '1', 'Codec': 'pngImage'}}
                   for name, path, pma in entries]
        self.description = 'Package.' + format
        if format == 'json':
            (self.source / self.description).write_text(json.dumps({
                'Resources': {'Resource': {'Path': 'Images/Images.json'}}}))
            (self.source / 'Images/Images.json').write_text(json.dumps({'Name': 'Test', 'Resource': records}))
        else:
            (self.source / self.description).write_text(
                '<Pak><Resources><Resource Path="Images/Images.xml"/></Resources></Pak>')
            root = ET.Element('DataBlock', Name='Test')
            for record in records:
                file = record.pop('File')
                ET.SubElement(ET.SubElement(root, 'Resource', record), 'File', file)
            ET.ElementTree(root).write(self.source / 'Images/Images.xml')

    def build(self, **options):
        with contextlib.redirect_stdout(io.StringIO()):
            return build_resource_pack(self.source, self.destination, description=self.description,
                                       img_premultiply=options.pop('img_premultiply', True), **options)

    def files(self):
        return {node.attrib['Name']: node.find('File').attrib
                for node in ET.parse(self.destination / 'Images/Images.xml').findall('Resource')}

class PngBuildTests(PngPackFixture, unittest.TestCase):
    def test_pma_activates_stage_and_tool_without_png_opt(self):
        project = Project()
        project.OnlyExe, project.NoExe, project.Zipout = False, True, None
        project.IsXlsxExport, project.IsCreatePacks = False, False
        project.imagePremultiply, project.IsPngOptimize = True, False
        project.IsMakeAtlas, project.IsHalfTextures = True, True
        builder = Builder()
        configureBuilderActions(builder, project)
        names = [type(action).__name__ for action in builder.actions]
        for following in ('BuilderActionMakeAtlas', 'BuilderActionPngResizer', 'BuilderActionBuildResources'):
            self.assertLess(names.index('BuilderActionPngOptimize'), names.index(following))
        self.assertIn('AlphaSpreading', required_tools_for_config({'img_premultiply': True, 'png_opt': False}))

    def test_plain_copy_does_not_require_converter(self):
        with patch.object(OSSystem, 'run_tool') as tool:
            self.build(img_premultiply=False)
        tool.assert_not_called()
        self.assertEqual(self.files()['Image']['Premultiply'], '0')
        self.assertEqual((self.destination / 'Images/icon.png').read_bytes(), self.original)

    def test_overlap_and_invalid_flags_are_rejected(self):
        for destination in (self.source, self.source / 'child', self.root):
            with self.subTest(destination=destination), self.assertRaises(ValueError):
                build_resource_pack(self.source, destination)
        with self.assertRaises(ValueError):
            self.build(img_premultiply='true')
        self.assertEqual(self.png.read_bytes(), self.original)

    def test_converter_failures_do_not_publish_or_leave_temporary_files(self):
        for failure in ((False, 'decode error', ''), (True, '', ''), OSError('cannot launch converter')):
            with self.subTest(failure=failure):
                options = {'side_effect': failure} if isinstance(failure, Exception) else {'return_value': failure}
                with patch('Builder.Toolchain.tool_path', return_value='AlphaSpreading'), \
                        patch.object(OSSystem, 'run_tool', **options), self.assertRaises(RuntimeError):
                    self.build()
                self.assertFalse((self.destination / self.description).exists())
                self.assertFalse((self.destination / 'Images/Images.xml').exists())
                self.assertFalse(list(self.root.glob('resource-build-*')))
                self.assertEqual(self.png.read_bytes(), self.original)

    def test_optimizer_rejects_source_overwrite_and_conflicting_outputs(self):
        optimizer = PngOptimizer(self.root)
        self.addCleanup(optimizer.cleanup)
        with self.assertRaises(ValueError):
            optimizer.optimize(self.png, self.png, True)
        destination = optimizer.output_path(self.png, True)
        optimizer.optimize(self.png, destination, True)
        with self.assertRaises(ValueError):
            optimizer.optimize(self.png, destination, False)

    def test_marked_pma_is_neither_spread_nor_premultiplied_again(self):
        self.package([('Image', 'Images/icon.png', '1')])
        with patch('Builder.Toolchain.tool_path', return_value='AlphaSpreading'), \
                patch.object(OSSystem, 'run_tool') as tool:
            self.build(png_opt=True)
        tool.assert_not_called()
        self.assertEqual(self.files()['Image']['Path'], 'Images/icon.png')
        self.assertEqual((self.destination / 'Images/icon.png').read_bytes(), self.original)


@unittest.skipUnless(os.environ.get('MENGINE_BUILDER_TOOL_ALPHASPREADING'),
                     'Set MENGINE_BUILDER_TOOL_ALPHASPREADING to a corrected native tool')
class NativePngBuildTests(PngPackFixture, unittest.TestCase):
    def test_rgb_input_becomes_opaque_rgba_with_matching_metadata(self):
        Image.new('RGB', (4, 1), (200, 100, 50)).save(self.png)
        declaration = self.source / 'Images/Images.xml'
        declaration.write_text(declaration.read_text().replace('Alpha="1"', 'Alpha="0"'))
        self.build()
        entry = self.files()['Image']
        self.assertEqual(entry['Alpha'], '1')
        with Image.open(self.destination / entry['Path']) as image:
            self.assertEqual(image.mode, 'RGBA')
            self.assertEqual(image.getpixel((0, 0)), (200, 100, 50, 255))

    def test_native_pma_pixels_metadata_aliases_and_cleanup(self):
        self.package([('First', 'Images/icon.png', '0'), ('Second', 'Images/icon.png', '0')])
        original_xml = (self.source / 'Images/Images.xml').read_bytes()
        with patch.object(OSSystem, 'run_tool', wraps=OSSystem.run_tool) as tool:
            self.build()
        self.assertEqual(tool.call_count, 1)
        entries = self.files()
        self.assertEqual(entries['First']['Path'], entries['Second']['Path'])
        self.assertEqual(entries['First']['Path'], 'Images/icon.png')
        self.assertEqual(entries['First']['Premultiply'], '1')
        with Image.open(self.destination / entries['First']['Path']) as image:
            self.assertEqual(list(image.get_flattened_data()),
                             [(0, 0, 0, 0), (64, 31, 15, 64), (128, 63, 31, 128), (255, 127, 63, 255)])
        self.assertEqual(self.png.read_bytes(), self.original)
        self.assertEqual((self.source / 'Images/Images.xml').read_bytes(), original_xml)
        self.assertNotIn('__Dir', (self.destination / 'Images/Images.xml').read_text())
        self.assertFalse(list(self.root.glob('resource-build-*')))
        self.assertEqual([p.relative_to(self.destination).as_posix()
                          for p in self.destination.rglob('*.png')], ['Images/icon.png'])

    def test_json_has_no_temporary_paths(self):
        self.package(format='json')
        self.build()
        text = (self.destination / 'Images/Images.json').read_text()
        record = json.loads(text)['Resource'][0]['File']
        self.assertEqual(record['Path'], 'Images/icon.png')
        self.assertEqual(record['Premultiply'], '1')
        self.assertTrue((self.destination / record['Path']).is_file())
        self.assertNotIn('__Dir', text)
        self.assertNotIn(str(self.root), text)

    def test_second_build_in_same_process_uses_current_source_and_project(self):
        self.build()
        old = self.destination
        self.destination = self.root / 'second'
        Image.new('RGBA', (4, 1), (200, 100, 50, 128)).save(self.png)
        self.build()
        with Image.open(self.destination / self.files()['Image']['Path']) as image:
            self.assertEqual(image.getpixel((0, 0)), (100, 50, 25, 128))
        with Image.open(old / 'Images/icon.png') as image:
            self.assertEqual(image.getpixel((0, 0)), (0, 0, 0, 0))

    def test_native_invalid_png_fails_without_publication(self):
        self.png.write_bytes(b'invalid PNG')
        with self.assertRaises(RuntimeError):
            self.build()
        self.assertFalse((self.destination / self.description).exists())
        self.assertFalse(list(self.root.glob('resource-build-*')))

    def test_spreading_keeps_visible_pixels_and_alpha(self):
        Image.new('RGBA', (4, 1), (200, 100, 50, 128)).save(self.png)
        self.build(img_premultiply=False, png_opt=True)
        entry = self.files()['Image']
        self.assertEqual(entry['Premultiply'], '0')
        self.assertEqual(entry['Path'], 'Images/icon.png')
        with Image.open(self.destination / entry['Path']) as image:
            self.assertEqual(image.getpixel((0, 0)), (200, 100, 50, 128))

    def test_different_conversion_parameters_do_not_share_results(self):
        optimizer = PngOptimizer(self.root)
        self.addCleanup(optimizer.cleanup)
        pma, spread = (optimizer.output_path(self.png, flag) for flag in (True, False))
        optimizer.optimize(self.png, pma, True)
        optimizer.optimize(self.png, spread, False)
        self.assertNotEqual(pma, spread)
        with patch.object(OSSystem, 'run_tool', wraps=OSSystem.run_tool) as tool:
            self.assertTrue(optimizer.flush())
        self.assertEqual(tool.call_count, 2)
        with Image.open(pma) as image:
            self.assertEqual(image.getpixel((1, 0)), (64, 31, 15, 64))
        with Image.open(spread) as image:
            self.assertEqual(image.getpixel((1, 0)), (255, 127, 63, 64))


if __name__ == '__main__':
    unittest.main()
