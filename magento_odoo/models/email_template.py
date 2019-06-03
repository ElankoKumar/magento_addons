from odoo import models,fields


class email_template(models.Model):
	_inherit = 'mail.template'
	_description = 'Magento Email Templates'

	is_magento = fields.Boolean("Is Magento ? ")
	magento_id = fields.Char("Magento ID ")
	



		

