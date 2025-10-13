
document.addEventListener('DOMContentLoaded', function() {
    const {createApp} = Vue;

    createApp({
        data() {
            return {
                baskets: [],
                loading: true,
            }
        },
        computed: {
            totalCount() {
                const count = this.baskets.reduce((total, basket) => total + basket.count, 0);
                console.log('totalCount вычислен:', count);
                return count;
            },
            totalPrice() {
                return this.baskets.reduce((total, basket) => total + (basket.price * basket.count), 0);
            },
            totalCountText() {
                const count = this.totalCount;
                if (count === 1) return 'товар';
                if (count >= 2 && count <= 4) return 'товара';
                return 'товаров';
            },

        },

        methods: {
            async loadBasket() {
                this.loading = true
                try {
                    const response = await fetch('api/basket/');
                    this.baskets = await response.json();
                } catch (error) {
                    console.log('Ошибка', error)
                }
                this.loading = false
                console.log(this.baskets)
            },
            getCSRFToken() {
                const cookieValue = document.cookie
                    .split('; ')
                    .find(row => row.startsWith('csrftoken='))
                    ?.split('=')[1];
                return cookieValue;
            },
            async removeFromBasket(basketId, type) {
                try {
                    const response = await fetch(`/api/basket/${basketId}/`, {
                        method: 'DELETE',

                        headers: {
                            'X-CSRFToken': this.getCSRFToken(),
                            'Content-Type': 'application/json'
                        },

                        body: JSON.stringify({
                            type: type
                        })
                    });
                    if (response.status === 204) {
                        await this.loadBasket()
                    } else if (response.status === 200) {
                        const updateItem = await response.json()

                        const index = this.baskets.findIndex(item => item.id === basketId)
                        this.baskets[index] = updateItem
                    }
                } catch (error) {
                    console.log('Ошибка', error)
                }
            },
            async addBasket(basketId, product) {
                const response = await fetch('api/basket/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': this.getCSRFToken(),
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        product: product,
                        basket: basketId
                    })
                });
                if (response.status === 200) {
                    const itemID = await response.json()
                    console.log(itemID)
                    const index = this.baskets.findIndex(item => item.id === basketId)
                    this.baskets[index] = itemID
                }

            },
            showNotification(message, type = 'success') {

                const notification = document.createElement('div');
                notification.textContent = message;
                notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 15px 20px;
                background: ${type === 'success' ? '#4CAF50' : '#f44336'};
                color: white;
                border-radius: 5px;
                z-index: 1000;
                animation: slideIn 0.3s ease;
            `;

                document.body.appendChild(notification);

                setTimeout(() => {
                    notification.remove();
                }, 3000);
            },
            async addBasketNew(event) {
                const productId = event.target.getAttribute('data-product-id');
                const response = await fetch('api/basket/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': this.getCSRFToken(),
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        product: parseInt(productId),
                    })
                });
                if (response.ok) {
                    this.showNotification('Товар добавлен в корзину!', 'success');
                    const item = await response.json()
                    const basketId = item.id
                    const index = this.baskets.findIndex(item=>item.id===basketId)
                    this.baskets[index] = item
                    console.log(item)

                } else {
                    this.showNotification('Ошибка при добавлении', 'error');
                }
            },

        },
        mounted() {
            this.loadBasket();
        }
    }).mount('#basket-app');
})