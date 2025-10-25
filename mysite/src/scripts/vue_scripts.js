
document.addEventListener('DOMContentLoaded', function() {
    const {createApp} = Vue;

    createApp({
        data() {
            return {
                baskets: [],
                loading: true,
                api: 'aad9b4e7-a06a-4ada-a44b-399f65afc8dc',
                geo: '',
                address: [],
                map: null, // Добавляем для хранения объекта карты
                mapInitialized: false, // Флаг инициализации карты
                coordinates: [55.755864, 37.617698], // Координаты по умолчанию (Москва)
                zoom: 10
            }
        },
        computed: {
            totalCount() {
                const count = this.baskets.reduce((total, basket) => total + basket.count, 0);
                console.log('totalCount вычислен:', count);
                return count;
            },
            totalPrice() {
                const price = this.baskets.reduce((total, basket) => total + basket.price * 1, 0);
                console.log('Сумма', price)
                if (price === 0) return 'Пусто'
                else return price
            },
            totalCountText() {
                const count = this.totalCount;
                if (count === 1) return 'товар';
                if (count >= 2 && count <= 4) return 'товара';
                return 'товаров';
            },

        },

        methods: {
            async geoDecode(){
                const response = await fetch(`https://geocode-maps.yandex.ru/v1/?apikey=aad9b4e7-a06a-4ada-a44b-399f65afc8dc&geocode=${this.geo}&format=json`)
                const data = await response.json()
                const features = data.response.GeoObjectCollection.featureMember;
                this.address = features.map(f => f.GeoObject.name)
                console.log(this.address)
            },
            async updateGeo(word) {
                this.geo = word
            },

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
                this.showNotification('Товары удалёны', 'error')
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
                    if (this.baskets.length > 0) {
                        const basketId = item.id
                        const index = this.baskets.findIndex(item=>item.id===basketId)
                        console.log(index)
                        if (index > 0) {
                            console.log('добавляем')
                            this.baskets[index] = item
                        }
                        else {
                            console.log('создаем')
                            await this.loadBasket()
                        }

                    }
                    else {
                        await this.loadBasket()
                    }


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