<template>

<form @submit.prevent="login">
    <h2>Login</h2>

    <input required type="text" name="email" id="email" v-model="email" placeholder="Email">
    <input required type="text" name="password" id="password" v-model="password" placeholder="Password">
    <button type="submit">Login</button>
</form>

</template>

<script>
import axios from 'axios';

export default{
data(){
    return{
        email:"",
        password:""
    }
},
methods:{
    async login(){
        const response = await axios.post('http://127.0.0.1:5000/login',
        {   email:this.email,
            password:this.password
        })
        const token = response.data.token
        localStorage.setItem('token', token);
        this.$router.push({ name: 'home' });
    }
}


}
</script>