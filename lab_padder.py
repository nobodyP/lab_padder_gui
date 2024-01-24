import os, glob
import click
from pathlib import Path

@click.command()
@click.option('--time', default=5000000, help='Time to pad labels')
@click.option('--phoneme', default='SP', help='Phoneme to use for padded silence')
@click.option('--lab_dir', '-d', required=True, help='Directory where your lab files are')
@click.option('--out', '-o', default='out', help='Directory where to save your lab files')

def main(time, phoneme, lab_dir, out):

	for label in glob.glob(f"{lab_dir}/*.lab", recursive=True):
		lab_list = []
		with open(label, 'r', encoding='utf-8') as lab:
			lab_list = [('0', f"{str(time)}", f"{phoneme}")]
			for line in lab:
				x1, x2, pho = line.rstrip().split(' ')
				x1 = int(x1) + time
				x2 = int(x2) + time
				lab_list.append((f"{str(x1)}", f"{str(x2)}", f"{pho}"))

			lab_list.append((f"{str(x2)}", f"{str(x2+time)}", f"{str(phoneme)}"))
			lab.close()

		p = Path(label)

		if not os.path.exists(out):
			os.mkdir(out)

		with open(f"{out}/{str(p.name)}", 'w+', encoding='utf-8') as olab:
			out_string = ''
			for i in range(len(lab_list)):
				out_string += f"{lab_list[i][0]} {lab_list[i][1]} {lab_list[i][2]}\n"
			olab.write(out_string)

if __name__ == "__main__":
	main()