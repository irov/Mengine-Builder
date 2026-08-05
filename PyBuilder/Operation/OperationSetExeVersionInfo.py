import datetime
import tempfile
from pathlib import Path

from PyBuilder.Error.ErrorHandler import ErrorHandler
from PyBuilder.FileSystem import FileSystem
from PyBuilder.Operation.Operation import Operation
from PyBuilder.OSSystem import OSSystem
from PyBuilder.Toolchain import CONSOLE_ROOT


class OperationSetExeVersionInfo(Operation):
    def _onParams(self, params):
        self.version = params.pop("Version")
        self.companyInfo = params.pop("CompanyInfo")
        self.sourcePath = params.pop("SourcePath")
        self.description = params.pop("Description")

    def _onRun(self):
        with tempfile.TemporaryDirectory(prefix="mengine-builder-rc-") as directory:
            compiler_resource = Path(directory) / "version.rc"
            resource = Path(directory) / "version.res"

            if self._createCompilerResourceFile(
                path=compiler_resource,
                version=self.version,
                originalFilename=self.description,
                internalName=self.description,
                description=self.description,
                companyName=self.companyInfo,
            ) is False:
                ErrorHandler.error("Resource file compilation error")
                return False

            if OSSystem.tool("rc", "-nologo", "/fo", resource, compiler_resource) is False:
                ErrorHandler.error("Resource compiler failed for `%s`" % compiler_resource)
                return False

            if OSSystem.tool(
                "ResourceHacker", "-open", self.sourcePath, "-save", self.sourcePath,
                "-action", "delete", "-mask", "VERSIONINFO",
            ) is False:
                ErrorHandler.error("Unable to delete VERSIONINFO from `%s`" % self.sourcePath)
                return False

            if OSSystem.tool(
                "ResourceHacker", "-open", self.sourcePath, "-save", self.sourcePath,
                "-action", "add", "-res", resource, "-mask", "VERSIONINFO",
            ) is False:
                ErrorHandler.error("Unable to add VERSIONINFO to `%s`" % self.sourcePath)
                return False

        return True

    def _createCompilerResourceFile(
        self,
        path,
        version,
        originalFilename,
        internalName,
        description,
        companyName,
        productName="",
    ):
        template_file = CONSOLE_ROOT / "resources" / "rc" / "template.rc"

        try:
            template = FileSystem.fileGetContents(template_file)
        except FileNotFoundError:
            ErrorHandler.error("File not found: %s" % template_file)
            return False

        content = template % (
            version,
            version,
            originalFilename,
            internalName,
            description,
            companyName,
            datetime.date.today().year,
            productName,
        )
        FileSystem.filePutContents(path, content, "w")
        return True
