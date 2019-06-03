from odoo import models,fields


class Invoice(models.Model):
	_inherit = 'account.invoice'
	_description = 'Magento Invoices'

	is_magento = fields.Boolean("Is Magento ? ")
	magento_id = fields.Char("Magento ID ")



		

