import opentimelineio as otio

timeline = otio.adapters.read_from_file("Input/Timeline.fcpxmld/Info.fcpxml")
print(timeline.video_tracks())
