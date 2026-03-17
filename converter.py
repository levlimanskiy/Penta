from pathlib import Path
import re, csv, difflib

DOC_TYPE_MAP = {
    'Сч-ф': 'Универсальный передаточный документ (счет-фактура)',
    'УПД':  'Универсальный передаточный документ (счет-фактура)',
    'Акт':  'Акт',
    }

def normalise_date(date_str: str) -> str:
    parts = date_str.split('.')
    if len(parts[2]) == 2:
        parts[2] = str(2000 + int(parts[2]))
    return '.'.join(parts)

# Classes 

class BudgetLookup:
    def __init__(self, csv_path: Path):
        self.csv_path = csv_path
        self.records = self._load()
    def _load(self):
        records = {}
        with open(self.csv_path, encoding='utf-8', newline='') as f:
            for row in csv.DictReader(f):
                key = row['inn'].strip() + '+' + row['kpp'].strip()
                rec = {
                    'status': row['status'].strip(),
                    'kbk':    row['kbk'].strip(),
                    'oktmo':  row['oktmo'].strip(),
                    'f42':    row['f42'].strip(),
                    'f43':    row['f43'].strip(),
                    'f44':    row['f44'].strip(),
                    'f45':    row['f45'].strip(),
                    'f46':    row['f46'].strip(),
                }
                records.setdefault(key, []).append(rec)
        return records
    def get(self, inn: str, kpp: str) -> list:
        key = inn + '+' + kpp
        return self.records.get(key, []) 


class ZRBlock:
    def __init__(self, zr_line: str):
        self.fields = zr_line.split('|')
    
    # fields actual names in this block
    @property
    def ref_number(self) -> str:
        return self.fields[2]
    @ref_number.setter
    def ref_number(self, value: str):
        self.fields[2] = value

    @property
    def record_number(self) -> str:
        return self.fields[3]
    
    @property
    def date_doc(self) -> str:
        return self.fields[4]
    
    @property
    def our_acc_name(self) -> str:
        return self.fields[7]
    
    @property
    def out_orgname_1(self) -> str:
        return self.fields[11]
    @out_orgname_1.setter
    def out_orgname_1(self, value: str):
        self.fields[11] = value

    @property
    def out_orgname_2(self) -> str:
        return self.fields[12]
    @out_orgname_2.setter
    def out_orgname_2(self, value: str):
        self.fields[12] = value

    @property
    def out_orgname_3(self) -> str:
        return self.fields[13]
    @out_orgname_3.setter
    def out_orgname_3(self, value: str):
        self.fields[13] = value

    @property
    def summa(self) -> str:
        return self.fields[23]
    
    @property
    def is_av(self) -> str:
        return self.fields[26]
    @is_av.setter
    def is_av(self, value: str):
        self.fields[26] = value

    @property
    def text(self) -> str:
        return self.fields[29]
    
    @property
    def recipient_name(self) -> str:
        return self.fields[31]

    @property
    def inn(self) -> str:
        return self.fields[32]
    
    @property
    def kpp(self) -> str:
        return self.fields[33]
    
    @property
    def lic_schet(self) -> str:
        return self.fields[34]
    @lic_schet.setter
    def lic_schet(self, value: str):
        self.fields[34] = value

    @property
    def acc_number(self) -> str:
        return self.fields[35]
    
    @property
    def bank_name(self) -> str:
        return self.fields[36]
    
    @property
    def bik(self) -> str:
        return self.fields[37]
    
    @property
    def corr_acc(self) -> str:
        return self.fields[38]
    
    @property
    def status(self) -> str:
        return self.fields[39]
    @status.setter
    def status(self, value: str):
        self.fields[39] = value

    @property
    def kbk(self) -> str:
        return self.fields[40]
    @kbk.setter
    def kbk(self, value: str):
        self.fields[40] = value
    
    @property
    def oktmo(self) -> str:
        return self.fields[41]
    @oktmo.setter
    def oktmo(self, value: str):
        self.fields[41] = value

    @property
    def zero_1(self) -> str:
        return self.fields[42]
    @zero_1.setter
    def zero_1(self, value: str):
        self.fields[42] = value
    
    @property
    def zero_2(self) -> str:
        return self.fields[43]
    @zero_2.setter
    def zero_2(self, value: str):
        self.fields[43] = value

    @property
    def zero_3(self) -> str:
        return self.fields[44]
    @zero_3.setter
    def zero_3(self, value: str):
        self.fields[44] = value

    @property
    def zero_4(self) -> str:
        return self.fields[45]
    @zero_4.setter
    def zero_4(self, value: str):
        self.fields[45] = value

    @property
    def zero_5(self) -> str:
        return self.fields[46]
    @zero_5.setter
    def zero_5(self, value: str):
        self.fields[46] = value

    @property
    def title_1(self) -> str:
        return self.fields[51]
    @title_1.setter
    def title_1(self, value: str):
        self.fields[51] = value

    @property
    def sign_1(self) -> str:
        return self.fields[52]

    @property
    def title_2(self) -> str:
        return self.fields[53]
    @title_2.setter
    def title_2(self, value: str):
        self.fields[53] = value

    @property
    def sign_2(self) -> str:
        return self.fields[54]
    
    @property
    def date_sign(self) -> str:
        return self.fields[55]

    @property
    def target_code(self) -> str:
        m = re.search(r'\((\d{2}-\d{2})\)', self.text.strip())
        return m.group(1) if m else ''

    @property
    def is_full(self) -> bool:
        return self.target_code != ''    

    def to_line(self) -> str:
        return '|'.join(self.fields)


class ZR3File:
    def __init__(self, path: Path):
        self.input_file = path
        self._read()

    def _read(self):
        content = self.input_file.read_bytes().decode('cp1251')
        self.lines = content.splitlines()
    
    def get_blocks(self) -> list:
        blocks = []
        for line in self.lines:
            if line.startswith('ZR|') and not line.startswith('ZROSN') and not line.startswith('ZRST'):
                blocks.append(ZRBlock(line))
        return blocks
    
    def write(self, output_path: Path, lines: list):
        content = '\r\n'.join(lines) + '\r\n'
        output_path.write_bytes(content.encode('cp1251'))


class Converter:
    def __init__(self, zr3file: ZR3File, budget_lookup: BudgetLookup, 
                 log_callback=None, choose_callback=None, choose_law=None):
        self.zr3file = zr3file
        self.budget_lookup = budget_lookup
        self.log = log_callback or print
        self.choose = choose_callback or self._choose_record_terminal
        self.choose_law = choose_law

    def convert(self) -> list:
        output_lines = []
        current_zrosn = []
        current_zrst = ''

        for line in self.zr3file.lines:
            if line.startswith('ZR|') and not line.startswith('ZROSN') and not line.startswith('ZRST'):
                block = self._process_block(line)
                current_zrosn = self._build_zrosn(block)
                output_lines.append(block.to_line())

            elif line.startswith('ZROSN'):
                pass

            elif line.startswith('ZRST'):
                if not block.is_full:
                    for idx, doc in enumerate(current_zrosn, start=1):
                        output_lines.append(
                            f"ZROSN|{idx}|{doc['type_label']}|{doc['num']}|{doc['date']}||"
                        )
                    current_zrosn = []
                    output_lines.append(line)
                else:
                    for doc in current_zrosn:
                        output_lines.append(
                            f"ZROSN||{doc['type_label']}|{doc['num']}|{doc['date']}|{doc['purpose']}|"
                        )
                    zrst_line = self._build_zrst(line, block)
                    output_lines.append(zrst_line)
                    current_zrosn = []
            else:
                output_lines.append(line)

        return output_lines

    def _process_block(self, line: str) -> ZRBlock:
        block = ZRBlock(line)
        
        if not block.is_full:
            if block.ref_number == '1':
                block.ref_number = '2'
            block.title_1 = ''
            block.title_2 = ''
            block.out_orgname_1 = ''
            block.out_orgname_2 = ''
            block.out_orgname_3 = ''

        if re.search(r'аванс', block.text, re.IGNORECASE):
            block.is_av = '1'

        if block.acc_number.startswith('031'):
            block.lic_schet = ''
            reqs = self.budget_lookup.get(block.inn, block.kpp)
            if not reqs:
                self.log(f'⚠️ No budget record for {block.inn}+{block.kpp}')
            else:
                rec = self.choose(block.record_number, block.recipient_name, reqs)
                block.status = rec['status']
                block.kbk    = rec['kbk']
                block.oktmo  = rec['oktmo']
                block.zero_1 = rec['f42']
                block.zero_2 = rec['f43']
                block.zero_3 = rec['f44']
                block.zero_4 = rec['f45']
                block.zero_5 = rec['f46']

        return block
  
    def _build_zrosn(self, block: ZRBlock) -> list:
        zrosn = []
        text = block.text

        if block.is_full:
            return self._build_zrosn_full(block)

        if block.acc_number.startswith('03'):
            contract = self._find_contract(text)
            if contract:
                zrosn.append(contract)
            zrosn.append({'type_label': 'УИН', 'num': '0', 'date': ''})

        elif block.text.strip().upper().startswith('УИН'):
            contract = self._find_contract(text)
            if contract:
                zrosn.append(contract)
            m = re.match(r'УИН\s+([^/\s]+)', text.strip(), re.IGNORECASE)
            uin_code = m.group(1) if m else '0'
            zrosn.append({'type_label': 'УИН', 'num': uin_code, 'date': ''})
        
        elif re.search(r'аванс', block.text, re.IGNORECASE):
            contract = self._find_contract(text)
            if contract:
                zrosn.append(contract)
            invoice = self._find_invoice(text)
            if invoice:
                zrosn.append(invoice)
        
        else:
            contract = self._find_contract(text)
            if contract:
                zrosn.append(contract)
            doc = self._find_act(text)
            if doc:
                zrosn.append(doc)
        return zrosn   
    
    def _build_zrosn_full(self, block: ZRBlock) -> list:
        zrosn = []
        text = block.text
        purpose = self._find_purpose(text)

        contract = self._find_contract(text)
        if contract:
            contract['purpose'] = purpose
            zrosn.append(contract)

        doc = self._find_act(text)
        if doc:
            doc['purpose'] = purpose
            zrosn.append(doc)

        invoice = self._find_invoice(text)
        if invoice:
            invoice['purpose'] = purpose
            zrosn.append(invoice) 


        if block.text.strip().upper().startswith('УИН'):
            m = re.match(r'УИН\s+([^/\s]+)', text.strip(), re.IGNORECASE)
            uin_code = m.group(1) if m else '0'
            zrosn.append({'type_label': 'УИН', 'num': uin_code, 'date': '', 'purpose': ''})

        return zrosn

    def _build_zrst(self, line: str, block: ZRBlock) -> str:
        if not block.is_full:
            return line
        fields = line.split('|')
        fields[6] = block.target_code
        fields[11] = self.choose_law(block.record_number, block.summa) if self.choose_law else ''
        return '|'.join(fields)

    def _find_contract(self, text: str):
        m = re.search(r'Дог\.N?\s*([\w\-/]+)\s+от\s+(\d{2}\.\d{2}\.\d{4})г?', text)
        if m:
            return {'type_label': 'Договор', 'num': m.group(1).strip(), 'date': m.group(2)}
        return None
    
    def _find_act(self, text: str):
        keywords = '|'.join(re.escape(k) for k in DOC_TYPE_MAP)
        m = re.search(
            rf'({keywords})[:\s]+([\w\-/]+)\s+от\s+(\d{{2}}\.\d{{2}}\.\d{{2,4}})г?',
            text
        )
        if m:
            return {
                'type_label': DOC_TYPE_MAP[m.group(1)],
                'num':  m.group(2).strip(),
                'date': normalise_date(m.group(3)),
            }
        return None

    def _find_invoice(self, text: str):
        m = re.search(r'[СCсc]ч(?:ет|\.)?\s*N?\s*([\w\-/]+)\s+от\s+(\d{2}\.\d{2}\.\d{2,4})г?', text)
        if m:
            return {'type_label': 'Счет', 'num': m.group(1).strip(), 'date': normalise_date(m.group(2))}
        return None
    
    def _find_purpose(self, text: str) -> str:
        m = re.search(
        r'[СCсc]ч(?:ет|\.)?\s*N?\s*[\w\-/]+\s+от\s+[\d\.]+г?[,.]?\s*(.+?)\s*(?:УПД|Акт|Сч-ф|[СCсc]ч-ф)',
        text,
        re.IGNORECASE
        )
        return m.group(1).strip() if m else ''
    
    def _choose_record_terminal(self,record_number: str, recipient_name: str, candidates: list) -> dict:
        if len(candidates) == 1:
            return candidates[0]
        name = recipient_name[:60] + '...' if len(recipient_name) > 60 else recipient_name
        self.log(f'\nЗКР {record_number} | {name} — какой КБК использовать?')
        for i, rec in enumerate(candidates, start=1):
            self.log(f'  {i}. КБК {rec["kbk"]}  ОКТМО {rec["oktmo"]}')
        while True:
            try:
                choice = int(input('Ваш выбор: '))
                if 1 <= choice <= len(candidates):
                    return candidates[choice - 1]
                self.log(f'  Введите число от 1 до {len(candidates)}')
            except ValueError:
                self.log('  Введите число')
    
    def preview(self) -> list:
        lines = []
        block = 0 
        for line in self.zr3file.lines:
            if line.startswith('ZR|') and not line.startswith('ZROSN') and not line.startswith('ZRST'):
                block += 1
                b = ZRBlock(line)
                is_budg = b.acc_number.startswith('031')
                is_adv  = bool(re.search(r'аванс', b.text, re.IGNORECASE))
                is_uin  = b.text.strip().upper().startswith('УИН')
                is_full = b.is_full
                ptype   = 'БЮДЖЕТНЫЙ' if is_budg else ('АВАНС' if is_adv else ('ПОЛНЫй' if is_full else('УИН' if is_uin else 'стандартный')))
                lines.append(f'ЗКР {b.record_number} [{ptype}] на {b.summa} р.:')
                for doc in self._build_zrosn(b):
                    lines.append(f'  → [{doc["type_label"]}]  {doc["num"]}  {doc["date"]}')
                if not self._build_zrosn(b):
                    lines.append('  ⚠️  No ZROSN built — check назначение платежа!')
        return lines