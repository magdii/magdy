from odoo import _, api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    @api.onchange('tax_field_per', 'wires_per', 'transportation_per', 'construction_per', 'guarantee_per',
                  'table_tax_per', 'amount_untaxed', 'added_value_tax_per')
    def _compute_values(self):
        self.tax_field = (self.tax_field_per * self.amount_untaxed) / 100
        self.wires = (self.wires_per * self.amount_untaxed) / 100
        self.transportation = (self.transportation_per * self.amount_untaxed) / 100
        self.construction = (self.construction_per * self.amount_untaxed) / 100
        self.guarantee = (self.guarantee_per * self.amount_untaxed) / 100

        self.invoice_devices = self.tax_field - self.wires - self.transportation - self.construction - self.guarantee

        self.table_tax = (self.invoice_devices * self.table_tax_per) / 100

        self.total_with_table_tax = self.table_tax + self.invoice_devices

        self.total_services = self.wires + self.transportation + self.construction + self.guarantee

        self.total_with_services = self.total_with_table_tax + self.total_services

        self.added_value_tax = (self.total_with_services * self.added_value_tax_per) / 100

        self.total_invoice = self.total_with_services + self.added_value_tax

    tax_field_per = fields.Float()
    wires_per = fields.Float()
    transportation_per = fields.Float()
    construction_per = fields.Float()
    guarantee_per = fields.Float()
    table_tax_per = fields.Float()
    added_value_tax_per = fields.Float()

    tax_field = fields.Float(compute='_compute_values')
    wires = fields.Float(compute='_compute_values')
    transportation = fields.Float(compute='_compute_values')
    construction = fields.Float(compute='_compute_values')
    guarantee = fields.Float(compute='_compute_values')
    invoice_devices = fields.Float(compute='_compute_values')
    table_tax = fields.Float(compute='_compute_values')
    total_with_table_tax = fields.Float(compute='_compute_values')
    total_services = fields.Float(compute='_compute_values')
    total_with_services = fields.Float(compute='_compute_values')
    added_value_tax = fields.Float(compute='_compute_values')
    total_invoice = fields.Float(compute='_compute_values')
