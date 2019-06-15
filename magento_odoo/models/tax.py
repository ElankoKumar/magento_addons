from odoo import models,fields


class Tax(models.Model):
	_inherit = 'account.tax'
	_description = 'Magento Taxes'

	is_magento = fields.Boolean("Is Magento ? ")
	magento_id = fields.Char("Magento ID ")



		

