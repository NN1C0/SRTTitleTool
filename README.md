# SRT to Final Cut Pro X
Can be used to convert SRT subtitles files to an FCPX timeline. Creates a new fcpxml that can be importet into FCPX.

## Requirements
Requires [LXML](https://pypi.org/project/lxml/) and [SRT](https://pypi.org/project/srt/)

## Usage

`python SRT_to_FCPXML.py`

```
-i --input      Path to subtitle.srt [default=input/subtitles.srt]
-o --output     Path to FCPXML [default=output/subtitles.fcpxml]
-f --framerate  Traget framerate of the timeline [default=25]
```

## Notes
Only tested under MacOS 14.0 and Final Cut 10.6.8