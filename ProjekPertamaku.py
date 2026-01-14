import json
import os
from datetime import datetime


DATA_FILE = 'finance_data.json'


def load_data():
	if not os.path.exists(DATA_FILE):
		return {'transactions': []}
	with open(DATA_FILE, 'r', encoding='utf-8') as f:
		return json.load(f)


def save_data(data):
	with open(DATA_FILE, 'w', encoding='utf-8') as f:
		json.dump(data, f, ensure_ascii=False, indent=2)


def add_transaction(data, kind):
	print(f"\nMenambah transaksi ({kind})")
	try:
		amount = float(input('Masukkan jumlah (contoh 150000.50): ').strip())
	except ValueError:
		print('Jumlah tidak valid.')
		return
	desc = input('Deskripsi singkat: ').strip()
	date_str = input('Tanggal (YYYY-MM-DD) [kosong=hari ini]: ').strip()
	if not date_str:
		date_str = datetime.today().strftime('%Y-%m-%d')
	else:
		try:
			datetime.strptime(date_str, '%Y-%m-%d')
		except ValueError:
			print('Format tanggal tidak benar. Gunakan YYYY-MM-DD.')
			return
	tx = {
		'date': date_str,
		'type': kind,
		'amount': amount,
		'desc': desc
	}
	data['transactions'].append(tx)
	save_data(data)
	print('Transaksi tersimpan.')


def summarize_month(data, year=None, month=None):
	if year is None or month is None:
		today = datetime.today()
		year = today.year
		month = today.month
	total_income = 0.0
	total_expense = 0.0
	items = []
	for tx in data.get('transactions', []):
		try:
			d = datetime.strptime(tx['date'], '%Y-%m-%d')
		except Exception:
			continue
		if d.year == int(year) and d.month == int(month):
			items.append(tx)
			if tx['type'] == 'income':
				total_income += float(tx['amount'])
			else:
				total_expense += float(tx['amount'])
	return total_income, total_expense, items


def show_summary(data):
	print('\n-- Ringkasan Bulanan --')
	ym = input('Masukkan bulan (YYYY-MM) [kosong=bulan ini]: ').strip()
	if ym:
		try:
			year, month = ym.split('-')
			year = int(year)
			month = int(month)
			if not (1 <= month <= 12):
				raise ValueError
		except Exception:
			print('Format salah. Gunakan YYYY-MM (mis. 2025-01).')
			return
	else:
		year = None
		month = None
	income, expense, items = summarize_month(data, year, month)
	print(f'Pemasukan: {income:,.2f}')
	print(f'Pengeluaran: {expense:,.2f}')
	print(f'Saldo: {income - expense:,.2f}')
	if items:
		print('\nDaftar transaksi:')
		for t in items:
			sign = '+' if t['type'] == 'income' else '-'
			print(f"{t['date']}  {sign}{t['amount']:,.2f}  {t['desc']}")
	else:
		print('Tidak ada transaksi untuk bulan ini.')


def list_all(data):
	print('\n-- Semua Transaksi --')
	txs = sorted(data.get('transactions', []), key=lambda x: x.get('date', ''))
	if not txs:
		print('Belum ada transaksi.')
		return
	for t in txs:
		print(f"{t['date']}  {t['type']:7}  {t['amount']:,.2f}  {t['desc']}")


def delete_last(data):
	if not data.get('transactions'):
		print('Tidak ada transaksi untuk dihapus.')
		return
	last = data['transactions'].pop()
	save_data(data)
	print('Terakhir dihapus:', last)


def main():
	data = load_data()
	print('Aplikasi Manajemen Keuangan - Sederhana')
	while True:
		print('\nMenu:')
		print('1) Tambah pemasukan')
		print('2) Tambah pengeluaran')
		print('3) Lihat ringkasan bulanan')
		print('4) Tampilkan semua transaksi')
		print('5) Hapus transaksi terakhir')
		print('6) Keluar')
		choice = input('Pilih (1-6): ').strip()
		if choice == '1':
			add_transaction(data, 'income')
		elif choice == '2':
			add_transaction(data, 'expense')
		elif choice == '3':
			show_summary(data)
		elif choice == '4':
			list_all(data)
		elif choice == '5':
			delete_last(data)
		elif choice == '6':
			print('Sampai jumpa!')
			break
		else:
			print('Pilihan tidak valid.')


if __name__ == '__main__':
	main()

