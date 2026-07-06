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
}

const PLACEHOLDER_CONTRACT_FORM_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 8, name: 'Copperfield Freight', status: 'Inactive' },
];

function usePlaceholderContractForm(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_CONTRACT_FORM_ROWS;
}
