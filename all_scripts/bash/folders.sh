mkdir $1
cd $1

mkdir all_scripts
echo "#all_scripts" > all_scripts/README.md

mkdir input_dir
echo "#input_dir" > input_dir/README.md

mkdir output_dir
echo "#output_dir" > output_dir/README.md

mkdir datasets
echo "#datasets" > datasets/README.md

cd all_scripts
mkdir bash
mkdir logs_out

cd ..
ls

