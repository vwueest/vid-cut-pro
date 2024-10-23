mkdir out; for inputfile in $(dir cuts); do ffmpeg -i $(pwd)/cuts/${inputfile} -c:v libvpx-vp9 -crf 0 -b:v `ffprobe -v error -select_streams v:0 -show_entries stream=bit_rate -of csv=s=x:p=0 $(pwd)/cuts/${inputfile}` -c:a libopus -b:a `ffprobe -v error -select_streams a:0 -show_entries stream=bit_rate -of csv=s=x:p=0 $(pwd)/cuts/${inputfile}` $(pwd)/out/${inputfile}.webm; done


#!/bin/bash

# Create output directory
mkdir -p $1/out

# Loop through all files in the cuts directory
for file_path in $1/cuts/*; do
	# Skip directories
	if [[ -d "${file_path}" ]]; then
		continue
	fi

	# Get video bitrate
	video_bitrate=$(ffprobe -v error -select_streams v:0 -show_entries stream=bit_rate -of csv=s=x:p=0 "${file_path}")

	# Get audio bitrate
	audio_bitrate=$(ffprobe -v error -select_streams a:0 -show_entries stream=bit_rate -of csv=s=x:p=0 "${file_path}")

	# Extract file name without extension
	file_name=${file_path##*/}
	file_name=${file_name%.*}

	# Extract directory name
	dir_name=${file_path%/*}

	# Remove directory name from file path
	filen_name_without_dir=${file_path#"${dir_name}/"}

	# Reencode video and audio with the same bitrate
	ffmpeg -i "${file_path}" -c:v libvpx-vp9 -crf 0 -b:v "${video_bitrate}" -c:a libopus -b:a "${audio_bitrate}" "$1/out/${filen_name_without_dir}.webm" -y
done
