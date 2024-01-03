import csv
import shutil

months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

def modify_second_line(file_name):
    temp_file = file_name + '.tmp'

    with open(file_name, 'r', newline='', encoding='latin-1') as file_read, \
         open(temp_file, 'w', newline='', encoding='latin-1') as file_write:

        line_count = 0
        for line in file_read:
            line_count += 1
            if line_count == 1:
                file_write.write('Data;Histórico;Docto.;Crédito (R$);Débito (R$);Saldo (R$);'  + '\n')
            elif line_count == 2:
                file_write.write(';;;;; \n')
            elif ';' not in line:
                break
            else:
                file_write.write(line)

    # Replace the original file with the modified temporary file
    shutil.move(temp_file, file_name)

def convert_to_float(s):
    parts = s.split('.')
    if len(parts) > 2:
        s = ''.join(parts[:-1]) + '.' + parts[-1]
    return float(s)
   
def get_total(file_name):
    total_spent = 0.0
    total_received = 0.0
    with open(file_name, newline='', encoding='latin-1') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            if 'Pix' in row['Histórico']:
                if row['Débito (R$)']:
                    debit_amount = float(row['Débito (R$)'].replace(".","").replace(',', '.').replace('"', ''))
                    total_spent += debit_amount
                if row['Crédito (R$)']:
                    credit_amount = float(row['Crédito (R$)'].replace(".","").replace(',', '.').replace('"', ''))
                    total_received += credit_amount

    total = total_received + total_spent
    return total


if __name__ == '__main__':
    for m in months:
        file_name = f'data_pix/{m}.csv' 
        modify_second_line(file_name)
        
        total = ('{:.2f}'.format(get_total(file_name))).replace('.',',')
        print(f"{m} pix total: R${total}")


