git add .
git commit -m "features and fixes"
git push
cp ~/RH-ota ~/RH-ota-bup
git checkout no_pdf_included
cd ~
rm -r ~/RH-ota-bup/.git
cp ~/RH-ota-bup ~/RH-ota
cd RH-ota
rm -r how_to
git add .
git commit -m "features and fixes"
git push
git checkout master