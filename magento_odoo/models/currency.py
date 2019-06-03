from datetime import timedelta
from odoo import models,fields


class Currency(models.Model):
	_inherit = 'res.currency'
	_description = 'Magento Currencies'

	is_magento = fields.Boolean("Is Magento ? ")
	magento_id = fields.Char("Magento ID ")
	



		

