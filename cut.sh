while IFS=',' read -r path rest
do
  echo "$path"
done < openimages_common_214_ram_annots.txt > openimages_214.txt
