import os

if __name__ == '__main__':
    files = os.listdir('icons/outline/svg/')
    print(files)
    with open('assets.qrc', 'w') as outFile:
        outFile.write('<!DOCTYPE RCC><RCC version="1.0">\n')
        outFile.write('<qresource>\n')
        for f in files:
            outFile.write(f'    <file alias="{f.replace("-outline", "")[:-4]}">icons/outline/svg/{f}</file>\n')
        outFile.write('</qresource>\n')
        outFile.write('</RCC>')
