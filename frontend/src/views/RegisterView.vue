<template>


<form @submit.prevent="register">
    <h2>Register</h2>

    <input required type="text" name="full_name" id="fullname" v-model="full_name" placeholder="Full Name">
    <input required type="text" name="email" id="email" v-model="email" placeholder="Email">
    <input required type="text" name="password" id="password" v-model="password" placeholder="Password">
    <button type="submit">Register</button>
    <router-link to="/login">Login</router-link>
    </form>

</template>

<script>
import axios from 'axios';

export default{
data(){
    return{
        email:"",
        password:"",
        full_name:""
    }
},
methods:{
    async register(){
        const response = await axios.post('http://127.0.0.1:5000/register',
        {   email:this.email,
            password:this.password,
            full_name:this.full_name
        })
        const token = response.data.token
        localStorage.setItem('token', token);
        this.$router.push({ name: 'login' });
    }
}


}
</script>