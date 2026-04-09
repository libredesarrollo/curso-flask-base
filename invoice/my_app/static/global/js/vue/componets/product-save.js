Vue.component('product-save', {
  props: {
    time: Number,
    productEdit: {
      type: Object,
      default: undefined
    }
  },
  data: function () {
    return {
      products: [],
      fcategory_id: 0,
      fname: "",
      fprice: 0,
      product: "",
      error:"",
      categories:[]
    }
  },
  created(){
    this.getCategories()
  },
  methods: {
    getCategories: function () {
      fetch('http://localhost:5000/api/categories/')
        .then(res => res.json())
        .then(res => {
          this.categories = res.data
        })
    },
    productSave: function () {
      var formData = new FormData()
      formData.append("name", this.fname)
      formData.append("price", this.fprice)
      formData.append("category_id", this.fcategory_id)

      this.error = ""

      if (this.productEdit) {
        this.productUpdate(formData)
      } else {
        this.productInsert(formData)
      }


    },
    productInsert(formData) {
      fetch('http://localhost:5000/api/products/', {
        method: 'POST',
        body: formData
      })
        .then(res => res.json())
        .then(res => {

          if(res.code == 200){
            this.product = res
            this.$emit("eventProductInsert", this.product)
            $("#saveModal").modal("hide")
          }else{
            this.error = res.msj
          }


        })
    },
    productUpdate(formData) {
      fetch('http://localhost:5000/api/products/'+this.productEdit.id, {
        method: 'PUT',
        body: formData
      })
        .then(res => res.json())
        .then(res => {
         if(res.code == 200){
            this.product = res
            this.$emit("eventProductUpdate", this.product)
            $("#saveModal").modal("hide")
          }else{
            this.error = res.msj
          }
        })
    }
  },
  watch: {
    time: function (newValue, oldValue) {
      this.error = ""
      $("#saveModal").modal("show")
      if (this.productEdit) {
        this.fname = this.productEdit.name
        this.fprice = this.productEdit.price
        this.fcategory_id = this.productEdit.category_id
      } else {
        this.fname = ""
        this.fprice = 0
        this.fcategory_id = 0
      }
    }
  },
  template:
    `
    <div class="modal fade" id="saveModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">Crear producto</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">

            <div v-if="error" class="alert alert-danger">
              {{ error }}
            </div>

            <div class="form-group">
                <label for="name">Nombre</label> 
                <input class="form-control" v-model="fname" type="text" value="">
            </div>
            
            <div class="form-group">
                <label for="price">Precio</label> 
                <input class="form-control" v-model="fprice" type="text" value="">
            </div>
            
            <div class="form-group">
                <label for="category_id">Categoría</label> 
                <select class="form-control" v-model="fcategory_id">
                <option v-for="c in categories" :value="c.id">{{ c.name }}</option>
                </select>
            </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-dismiss="modal">Cerrar</button>
          <button v-on:click="productSave" class="btn btn-success">Enviar</button>
        </div>
      </div>
    </div>
  </div>
    
    `
});