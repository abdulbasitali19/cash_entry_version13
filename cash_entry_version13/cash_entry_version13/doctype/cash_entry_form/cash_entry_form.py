# Copyright (c) 2024, abdul basit ali and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CashEntryForm(Document):
    def on_submit(self):
        self.create_journal_entry_on_submit()
    
    def on_cancel(self):
        self.cancel_created_journal_entry()
    
    def cancel_created_journal_entry(self):
        doc = frappe.get_doc("Journal Entry", self.number)
        if doc.docstatus == 1:
            doc.cancel()
    
    def create_journal_entry_on_submit(self):
        doc = frappe.new_doc("Journal Entry")
        doc.posting_date = self.date
        doc.voucher_type = "Journal Entry"
        
        # Calculate total debit amount
        total_debit = sum(entry.get("amount") for entry in self.accounting_entries)
        
        # Add Cash/Bank entry
        doc.append("accounts", {
            "account": self.cashbank,
            "cost_center": self.accounting_entries[0].get("branch"),  # Assuming all entries have the same branch
            "user_remark": "",
            "credit_in_account_currency": total_debit,
            "reference_type": ""
        })
        
        # Add other accounting entries
        for entry in self.accounting_entries:
            doc.append("accounts", {
                "account": entry.get("account_name"),
                "cost_center": entry.get("branch"),
                "user_remark": entry.get("description"),
                "debit_in_account_currency": entry.get("amount"),
                "reference_by_user": entry.get("reference")
            })
        
        # Submit the Journal Entry
        doc.submit()    
        
        # Update the Cash Entry Form with the journal entry number
        frappe.db.set_value("Cash Entry Form", self.name, "number", doc.name)
        frappe.db.commit()
