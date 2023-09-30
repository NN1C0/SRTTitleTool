# SRT to Final Cut Pro X
Because the subtitle support in Apples Final Cut Pro has been lacking any attention of the developer team for the last 15 years, this tool can do what you want to do ✨*editable styles for subtitles*✨. 
Use it to convert a SubRip subtitle file to basic titles in Final Cut.
Works by creating a fcpxml which you can import into Final Cut. Copy all titles and paste them into your working timeline.

## Requirements
Requires [LXML](https://pypi.org/project/lxml/) and [SRT](https://pypi.org/project/srt/)
```
$ pip install lxml
$ pip install srt
```


## Usage

`$ python SRT_to_FCPXML.py`

```
-i --input      Path to subtitle.srt [default=input/subtitles.srt]
-o --output     Path to FCPXML [default=output/subtitles.fcpxml]
-f --framerate  Traget framerate of the timeline [default=25]
```

## Notes
Only tested under MacOS 14.0 and Final Cut 10.6.8