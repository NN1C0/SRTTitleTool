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
    parser.add_argument(#TODO: Implement input file path and check for existence
        '-i',
        '--input',
        type=str,
        required=False,
        default='input/subtitles.srt',
        help='SRT file to read'
    )
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        required=False,
        default='output/subtitles.fcpxml',
        help="Timeline file to write out."
    )
    parser.add_argument(
        '-f',
        '--framerate',
        type=int,
        required=False,
        default=25,
        help="Target framerate"

    )
    return parser.parse_args()


def buildBaseXML(subtitles, fps):
    outline = (
        E.fcpxml(
            E.resources(
                E.format(id="r1", name="FFVideoFormat1080p"+str(fps)),
                E.effect(id="r2", name="Basic Title", uid=".../Titles.localized/Bumper:Opener.localized/Basic Title.localized/Basic Title.moti"),
            ),
            E.project(
                E.sequence(
                    E.spine(
                        E.gap(
                        
                        name="Gap", duration=convertSecondsToFCPXseconds(getSubtitlesTotalDuration(subtitles), 25))
                    ),
                format="r1"),
            name="Subtitles"),
        version="1.11")
    )
    return ET.tostring(outline)

def addSubtiltesToXML(xmlOutline, subs):
    xmlString = ET.fromstring(xmlOutline)
    timelineRoot = xmlString.find(".//gap")

    for i, s in enumerate(subs):
        timelineRoot.append(E('title',
            E('text',
                E('text-style', s.content, ref="ts1"),
            ),
            ref="r2", lane="1", offset=SRTTimeToFCPXseconds(s.start, 25), start=SRTTimeToFCPXseconds(s.start, 25), duration=convertSecondsToFCPXseconds(getSubtitleDuration(s), 25))
        )
    #Attach the text style. Can only be in the defined once in the XML
    timelineRoot.find(".//title").append(
        E('text-style-def',
            E('text-style', font="Helvetica", fontSize="63", fontFace="Regular", fontColor="1 1 1 1", alignment="center" ),
        id="ts1"))
    return xmlString


def writeFCPXML(content, path):
    f = open(path, "wb")
    f.write(content)
    f.close()

def srtToString(subtitlesObject):
    return srt.compose(subtitlesObject)

def parseSRTFile(srtPath):
    try:
        with open(srtPath) as f:
            data = f.read()
            return list(srt.parse(data))
    except FileNotFoundError:
        raise Exception("No input file found for given path.")
    except srt.SRTParseError:
        raise Exception("SRT file not suitable. Check formatting etc.")


def getSubtitlesTotalDuration(subs):
    return subs[-1].end.total_seconds()

def getSubtitleDuration(sub):
    return (sub.end - sub.start).total_seconds()

def convertSecondsToFCPXseconds(s, fps):
    multiplier = fpsToMultiplier(fps)
    frac = Fraction(roundToMultipe(s, multiplier)).limit_denominator(100000)
    return str(frac.numerator) + "/" + str(frac.denominator) + "s"

def SRTTimeToFCPXseconds(s, fps):
    return convertSecondsToFCPXseconds(s.total_seconds(), fps)

def roundToMultipe(s,m):
    return round(s / m) * m

def fpsToMultiplier(fps):
    return round(1/fps, 4)

def main():
    args = parse_args()
    subtitles = parseSRTFile(args.input)
    outputFile = args.output
    fps = args.framerate
    
    xml = buildBaseXML(subtitles, fps)
    populatedXML = addSubtiltesToXML(xml, subtitles)

    xml = ET.tostring(populatedXML, encoding="UTF-8", doctype="<!DOCTYPE fcpxml>", pretty_print=True)
    writeFCPXML(xml, outputFile)


if __name__ == '__main__':
    main()