from odoo import models,fields


class CouponPrograms(models.Model):
	_name = 'coupon.programs'
	_description = 'Magento Coupons'
	_rec_name = 'coupon_code'

	periods = fields.Selection([('day' , 'DAY'),('month', 'MONTH'),('year' , 'YEAR')],string="Period",default='day')
	expiration_date = fields.Date("Expiry")	
	is_magento = fields.Boolean("Is Magento ? ")
	magento_id = fields.Char("Magento ID ")
	coupon_code = fields.Char("Coupon Code")
	times_used = fields.Integer("Times Used")
	usage_per_customer = fields.Integer("Usage per Customer")
	rule_id = fields.Integer("Rule ID")
	is_primary = fields.Boolean("Is Primary")
	
	



		

