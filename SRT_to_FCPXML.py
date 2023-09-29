import argparse
from argparse import RawTextHelpFormatter
from lxml import etree as ET
from lxml.builder import E


def parse_args():
    """ parse arguments out of sys.argv """
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '-i',
        '--input',
        type=str,
        required=True,
        help='SRT file to read'
    )
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        required=False,
        help="Timeline file to write out."
    )
    return parser.parse_args()


def build_base_XML():
    outline = (
        E.fcpxml(
            E.resources(
                E.format(id="r1", name="FFVideoFormat1080p25"),
                E.effect(id="r2", name="Basic Title", uid=".../Titles.localized/Bumper:Opener.localized/Basic Title.localized/Basic Title.moti"),
            ),
            E.project(
                E.sequence(
                    E.spine(),
                format="r1"),
            name="Subtitles"),
        version="1.11")
    )

    return outline

def writeFCPXML(content, path="Subtitles.fcpxml"):
    f = open(path, "wb")
    f.write(content)
    f.close()

def main():
    xml = ET.tostring(build_base_XML(), encoding="UTF-8", doctype="<!DOCTYPE fcpxml>", pretty_print=True)
    writeFCPXML(xml)


if __name__ == '__main__':
    main()