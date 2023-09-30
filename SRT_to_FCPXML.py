import argparse
from argparse import RawTextHelpFormatter
from fractions import Fraction
from lxml import etree as ET
from lxml.builder import E
import srt


def parse_args():
    """ parse arguments out of sys.argv """
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '-i',
        '--input',
        type=str,
        required=False,
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


def buildBaseXML(subtitles):
    outline = (
        E.fcpxml(
            E.resources(
                E.format(id="r1", name="FFVideoFormat1080p25"),
                E.effect(id="r2", name="Basic Title", uid=".../Titles.localized/Bumper:Opener.localized/Basic Title.localized/Basic Title.moti"),
            ),
            E.project(
                E.sequence(
                    E.spine(
                        E.gap(
                        
                        name="Gap", duration=convertSecondsToFCPXseconds(getSubtitlesTotalDuration(subtitles)))
                    ),
                format="r1"),
            name="Subtitles"),
        version="1.11")
    )
    return ET.tostring(outline)

def addSubtiltesToXML(xmlOutline, subs): #Try this: https://stackoverflow.com/questions/75397711/lxml-create-multiple-tags-while-looping-through-a-list-in-csv
    xmlString = ET.fromstring(xmlOutline)
    timelineRoot = xmlString.find(".//gap")

    for i, s in enumerate(subs):
        timelineRoot.append(E('title',
            E('text',
                E('text-style', s.content, ref="ts1"),
            ),
            ref="r2", lane="1", offset=SRTTimeToFCPXseconds(s.start, 25), start=SRTTimeToFCPXseconds(s.start, 25), duration=convertSecondsToFCPXseconds(getSubtitleDuration(s)))
        )
    #Attach the text style. Can only be in the defined once in the XML
    timelineRoot.find(".//title").append(
        E('text-style-def',
            E('text-style', font="Helvetica", fontSize="63", fontFace="Regular", fontColor="1 1 1 1", alignment="center" ),
        id="ts1"))
    return xmlString


def writeFCPXML(content, path="Output/Subtitles.fcpxml"):
    f = open(path, "wb")
    f.write(content)
    f.close()

def srtToString(subtitlesObject):
    return srt.compose(subtitlesObject)

def parseSRTFile(srtPath):
    with open(srtPath) as f:
        data = f.read()
    return list(srt.parse(data))

def getSubtitlesTotalDuration(subs):
    return subs[-1].end.total_seconds()

def getSubtitleDuration(sub):
    return (sub.end - sub.start).total_seconds()

def convertSecondsToFCPXseconds(s):
    frac = Fraction(roundToMultipe(s, 0.04)).limit_denominator(100000)
    return str(frac.numerator) + "/" + str(frac.denominator) + "s"

def SRTTimeToFCPXseconds(s, fr):
    return convertSecondsToFCPXseconds(s.total_seconds())

def roundToMultipe(s,m):
    return round(s / m) * m

def main():
    args = parse_args()
    
    if(not args.input):
        subtitles = parseSRTFile("input/example.srt")
    else:
        subtitles = parseSRTFile(args.input)

    
    xml = buildBaseXML(subtitles)
    populatedXML = addSubtiltesToXML(xml, subtitles)
    #print(ET.tostring(populatedXML))

    xml = ET.tostring(populatedXML, encoding="UTF-8", doctype="<!DOCTYPE fcpxml>", pretty_print=True)
    writeFCPXML(xml)


if __name__ == '__main__':
    main()