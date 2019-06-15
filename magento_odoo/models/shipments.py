from odoo import models,fields


class Shipments(models.Model):
	_name = 'shipment.shipment'
	_description = 'Magento Shipments'
	_rec_name = 'packing_slip'


	is_magento = fields.Boolean("Is Magento ? ")
	magento_id = fields.Char("Magento ID ")
	packing_slip = fields.Char("Packing Slip")
	order = fields.Many2one('sale.order',"Order")
	order_date = fields.Date("Order Date")
	sold_to = fields.Text("Sold To")
	ship_to = fields.Text("Ship To")
	payment_method = fields.Selection([('check','Check'),('money_order','Money order')],"Payment Method")
	shipping_method = fields.Selection([('dhl','DHL'),('United_Parcel_Service ','United Parcel Service')],"Shipping Method")
	
	

	shipment_one2many = fields.One2many('ship.ship','shipment_many2one',string = "shipment")

class ship(models.Model):
	_name = 'ship.ship'
	_description = 'shipment orders'

	shipment_many2one = fields.Many2one('shipment.shipment',string = "ship")
	quantity = fields.Char("Qty")
	products = fields.Char("Products")
	sku = fields.Char("SKU")


		

