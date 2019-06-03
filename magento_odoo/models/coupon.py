from odoo import models,fields


class CouponPrograms(models.Model):
	_name = 'coupon.programs'
	_description = 'Magento Coupons'

	periods = fields.Selection([('day' , 'DAY'),('month', 'MONTH'),('year' , 'YEAR')],string="Period",default='day')
	start_date = fields.Date("From")
	end_date = fields.Date("To")	
	is_magento = fields.Boolean("Is Magento ? ")
	magento_id = fields.Char("Magento ID ")
	coupon_code = fields.Char("Coupon Code")
	
	



		

