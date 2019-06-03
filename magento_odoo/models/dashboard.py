from odoo import fields,models,api

class MagentoDashboard(models.Model):
	_name = 'magento.dashboard'
	_description = "Magento Dashboard"
	_rec_name = 'rec_type'


	rec_type = fields.Selection([
		('sale_order','SALE ORDERS'),
		('customer','CUSTOMERS'),
		('products','PRODUCTS'),
		('invoices','INVOICES'),
		('shipments','SHIPMENTS'),
		('categories','CATEGORIES')
		],"Types")
	rec_count = fields.Integer()



	@api.multi
	def get_count_data(self):
		print("Counting the Records Count")
		if self.rec_type == 'customer':
			count = self.env['res.partner'].sudo().search_count(['&',('is_magento','=',True),('magento_id','!=',False)])
			self.write({'rec_count':count})
		if self.rec_type == 'products':
			count = self.env['product.template'].sudo().search_count(['&',('is_magento','=',True),('magento_id','!=',False)])
			self.write({'rec_count':count})

		if self.rec_type == 'sale_order':
			count = self.env['sale.order'].sudo().search_count(['&',('is_magento','=',True),('magento_id','!=',False)])
			self.write({'rec_count':count})

		if self.rec_type == 'invoices':
			count = self.env['account.invoice'].sudo().search_count(['&',('is_magento','=',True),('magento_id','!=',False)])
			self.write({'rec_count':count})

		if self.rec_type == 'shipments':
			count = self.env['shipment.shipment'].sudo().search_count(['&',('is_magento','=',True),('magento_id','!=',False)])
			self.write({'rec_count':count})

		if self.rec_type == 'categories':
			count = self.env['product.category'].sudo().search_count(['&',('is_magento','=',True),('magento_id','!=',False)])
			self.write({'rec_count':count})