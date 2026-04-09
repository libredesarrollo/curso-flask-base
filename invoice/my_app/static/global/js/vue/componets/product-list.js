Vue.component('product-list',{
    data: function(){
        return {
            products: [],
            productSelected:undefined,
            productIndexSelected:0,
            timeDelete:0,
            timeSave:0
        }
    },
    mounted(){
        this.findAll();
    },
    methods:{
        findAll: function(){
            console.log("Hola Mundo")
            this.message = "Me diste un click!"

            fetch('http://localhost:5000/api/products/')
            .then(res => res.json())
            .then(res => this.products = res)

        },
        productDelete: function(product,index){
            this.timeDelete = new Date().getTime()
            this.productSelected = product
            this.productIndexSelected = index
        },
        productSave: function(){
            this.productSelected = undefined
            this.timeSave = new Date().getTime()
        },
        productUpdate: function(product,index){
            this.productSelected = product
            this.productIndexSelected = index
            this.timeSave = new Date().getTime()
        },
        eventProductDelete: function(){
            console.log("Eliminado")
            this.$delete(this.products.data,this.productIndexSelected)
        },
        eventProductInsert: function(product){
            console.log(product.data.name)
            this.products.data.push(product.data)
        },
        eventProductUpdate: function(product){
            this.products.data[this.productIndexSelected].name = product.data.name
            this.products.data[this.productIndexSelected].category = product.data.category
            this.products.data[this.productIndexSelected].category_id = product.data.category_id
            this.products.data[this.productIndexSelected].price = product.data.price
        }
    },
    template:
    `
        <div>
            <button class="btn btn-success" v-on:click="productSave">Crear</button>
            <div v-if="products.length == 0">
                <h1>NO hay productos</h1>
            </div>
            
            <div v-else><h1>Productos</h1></div>

            <div v-for="(product, index) in products.data" class="jumbotron pb-2 pt-3">

                    <h3>
                        <a href="#">
                            {{ product.name }}
                        </a>
                    </h3>

                    <h5>{{ product.category }}</h5>

                    <a  v-on:click="productUpdate(product,index)" data-toggle="tooltip" data-placement="top" title="Editar" class="btn btn-success btn-sm" href="#"><i class="fa fa-edit"></i></a>

                    <button v-on:click="productDelete(product,index)" :data-name="product.name" :data-id="product.id" class="btn btn-danger btn-sm"><i  data-toggle="tooltip"  :title="'Eliminar producto '+product.name" data-placement="top"class="fa fa-trash"></i></button>
                </div>

                <product-delete v-on:eventProductDelete="eventProductDelete" :time="timeDelete" :product="productSelected" ></product-delete>
                <product-save v-on:eventProductUpdate="eventProductUpdate" v-on:eventProductInsert="eventProductInsert" :productEdit="productSelected" :time="timeSave" ></product-save>
        </div>
    
    `
});