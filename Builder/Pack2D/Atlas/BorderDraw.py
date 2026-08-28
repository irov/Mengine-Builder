from Builder import Tools

from Builder.Pack2D.Atlas.Field2D import Field2D

class BorderDraw(object):
    def draw(self, atlasImage, border):
        return self._onDraw(atlasImage, border)
        pass

    def _onDraw(self, atlasImage, border):
        raise NotImplementedError()
        pass
    pass

class BorderDrawRectangle(BorderDraw):
    def _onDraw(self, atlasImage, border):
        newWidth = atlasImage.width + border.width
        newHeight = atlasImage.height + border.height

        newImage = Tools.createImage(newWidth, newHeight, 4, (0,0,0,0))

        img = atlasImage.getImagePIL()
        Tools.pasteImage(newImage, img, border.left, border.top)
        rightEdge = newWidth - 1
        bottomEdge = newHeight - 1

        draw = ImageDraw.Draw(newImage)
        if border.left != 0:
            line = [(0,0), (0, bottomEdge)]
            draw.line(line, fill = border.color, width = border.left)
            pass
        if border.top != 0:
            line = [(0, 0), (rightEdge, 0)]
            draw.line(line, fill = border.color, width = border.top)
            pass
        if border.right != 0:
            line = [(rightEdge,0), (rightEdge, bottomEdge)]
            draw.line(line, fill = border.color, width = border.right)
            pass
        if border.bottom != 0:
            line = [(0,bottomEdge) , (rightEdge, bottomEdge)]
            draw.line(line, fill = border.color, width = border.bottom)
            pass

        return newImage
        pass
    pass

class BorderDrawEdge(BorderDraw):
    def _onDraw(self, atlasImage, border):
        newWidth = atlasImage.width + border.width
        newHeight = atlasImage.height + border.height

        newImage = Tools.createImage(newWidth, newHeight, 4, (0,0,0,0))

        img = atlasImage.getImagePIL()
        Tools.pasteImage(newImage, img, border.left, border.top)
        data = Tools.getImageData(newImage)
        field2D = Field2D(data, newWidth, newHeight)
        #print(self.height,newHeight)
        #Copying data to box around
        if border.top != 0:
            #print("copy top")
            #top Lines
            sourceLine = border.top
            lineNumbers = range(0, sourceLine)
            self.copyLines(field2D, sourceLine, lineNumbers)
            pass

        if border.bottom != 0:
            #print("copy bottom")
            #bottom lines+
            sourceLine = atlasImage.height + border.top - 1
            lineNumbers = range(sourceLine + 1, newHeight)

            self.copyLines(field2D, sourceLine, lineNumbers)
            pass

        if border.left != 0:
            #print("copy left")
            #left columns
            sourceColumn = border.left
            columnNumbers = range(0, sourceColumn)
            self.copyColumns(field2D, sourceColumn, columnNumbers)
            pass

        if border.right != 0:
            #print("copy right")
            #right columns
            sourceColumn = atlasImage.width + border.left - 1
            columnNumbers = range(sourceColumn + 1, newWidth)

            self.copyColumns(field2D, sourceColumn, columnNumbers)
            pass

        Tools.putImageData(newImage, data)
        return newImage
        pass

    def copyLines(self, field2D, sourceLineNumber, lineNumbers):
        for lineNumber in lineNumbers:
            #print("copyLine",sourceLineNumber,lineNumber)
            field2D.copyLine(field2D,sourceLineNumber,lineNumber)
            pass
        pass

    def copyColumns(self, field2D, sourceColumnNumber, columnNumbers):
        for columnNumber in columnNumbers:
            #print("copyColumn",sourceColumnNumber,columnNumber)
            field2D.copyColumn(field2D, sourceColumnNumber, columnNumber)
            pass
        pass
    pass
