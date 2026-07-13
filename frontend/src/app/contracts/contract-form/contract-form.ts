import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';

import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { ContractService } from '../../core/services/contract.service';
import { VendorService } from '../../services/vendor';

@Component({
  selector: 'app-contract-form',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule, Card, Button],
  templateUrl: './contract-form.html',
  styleUrls: ['./contract-form.css']
})
export class ContractForm implements OnInit {
  isEdit = false;
  contractId: number | null = null;
  contract: any = {
    contract_title: '',
    vendor_id: null,
    contract_type: 'Master Agreement',
    procurement_category: '',
    start_date: '',
    end_date: '',
    contract_value: null,
    payment_terms: 'Net 30',
    sla_details: '',
    warranty_details: '',
    responsible_manager: '',
    status: 'Draft'
  };
  vendors: any[] = [];
  documentFile: File | null = null;
  loading = true;
  saving = false;
  errorMsg = '';
  fileError = '';
  contractTypes = ['Master Agreement', 'Rate Contract', 'Service Level Agreement', 'Supply Agreement', 'NDA'];
  paymentTermOptions = ['Net 15', 'Net 30', 'Net 45', 'Net 60', 'Advance', 'Milestone Based'];
  categories = ['IT Equipment', 'Software Licenses', 'Cloud Services', 'Raw Materials',
                'Office Supplies', 'Furniture', 'Packaging', 'Logistics', 'Safety', 'Consumables'];
  statuses = ['Draft', 'Active', 'Expiring Soon', 'Expired', 'Renewed', 'Terminated'];
}

const PLACEHOLDER_CONTRACT_FORM_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 6, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 7, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 8, name: 'Northwind Steel', status: 'Active' },
];

function usePlaceholderContractForm(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_CONTRACT_FORM_ROWS;
  }
  return rows.filter((row) => !!row);
}
