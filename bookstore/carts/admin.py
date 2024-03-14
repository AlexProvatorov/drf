from django.contrib import admin
from carts.models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = [
        'customer',
        'item',
        'count',
        'created_at',
        'status',
    ]
    list_editable = ['status']
    ordering = ['-created_at', 'item']
    list_display_links = ('customer', 'item')
    actions = ['set_completed_status', 'set_cancelled_status']

    class Meta:
        model = Cart

    @admin.action(description='Подтвердить оплату')
    def set_completed_status(self, request, order_positions):
        for order_position in order_positions:
            order_position.item.count_in_stock -= order_position.count
            order_position.status = 'COMPLETED'
            order_position.item.save()
            order_position.save()

    @admin.action(description='Отклонить оплату')
    def set_cancelled_status(self, request, order_positions):
        order_positions.update(status='CANCELLED')
