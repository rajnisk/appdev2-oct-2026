<template>
    <h1>Home</h1>
    <p>Welcome, {{ name }}!</p>
    <p> {{ msg }}!</p>
    <button class="btn btn-danger" @click="logout()">Logout</button> 
    <br>
    <input type="text"  v-model="name">
    <button @click="fetchTasks">click me</button>  
    <button @click="addNum()">click to add</button> 
    <tr>
        <td>id</td>
        <td>title</td>
        <td>description</td>
        <td>delete</td>
        <td>update</td>
    </tr>

    <tr v-for="task in tasks">
        <td>{{ task.id }}</td>
        <td>{{ task.title }}</td>
        <td>{{ task.description }}</td>
        <td @click="deleteTask(task.id)">delete</td>
        <td @click="updateTask(task.id)">update</td>
    </tr>


<form @submit.prevent="addTask">
    <input type="text" placeholder="Task title" v-model="newTaskTitle">
    <input type="text" placeholder="Task description" v-model="newTaskDescription">
    <input type="number" placeholder="assigned to" value=1 v-model="user_id">
    <button type="submit">Add Task</button>
</form>

<form @submit.prevent="updateTask">
    <input type="text" placeholder="Task title" v-model="newTaskTitle">
    <input type="text" placeholder="Task description" v-model="newTaskDescription">
    <input type="number" placeholder="assigned to" value=1 v-model="user_id">
</form>


</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
     name:"John Doe",
     msg: "",
    tasks: [],
    newTaskTitle:"",
    newTaskDescription:"",
    user_id:""
    }
  },

  methods: {
    updateName() {
        alert(this.name)
      this.name = "Jane Smith";
    },

    async helloworld(){

        const res = await axios.get('http://127.0.0.1:5000/helloworld')
        this.msg = res.data.message

    },

    async fetchTasks(){
        const token = localStorage.getItem('token');
        const res = await axios.get('http://127.0.0.1:5000/tasks',{
            headers: {
                'Authorization': 'Bearer ' + token
            }
        })
        this.tasks = res.data.tasks
    },
    async deleteTask(id){
        const token = localStorage.getItem('token');

        const res = await axios.delete('http://127.0.0.1:5000/task/'+id, {
            headers: {
                'Authorization': 'Bearer ' + token
            }
        })
        this.fetchTasks()

    },
    async addTask(id){
                const token = localStorage.getItem('token');

        const res = await axios.post('http://127.0.0.1:5000/tasks',
        {   title:  this.newTaskTitle,
            description:    this.newTaskDescription,
            assigned_to: this.user_id
        },{
            headers: {
                'Authorization': 'Bearer ' + token
            }
        })
        this.fetchTasks()
    },
        async updateTask(id){
        const token = localStorage.getItem('token');
        const res = await axios.put('http://127.0.0.1:5000/task/'+id,
        {   title:  this.newTaskTitle,
            description:    this.newTaskDescription,
            assigned_to: this.user_id
        }, {
            headers: {
                'Authorization': 'Bearer ' + token
            }
        })
        this.fetchTasks()

    },
        checkToken(){
        const token = localStorage.getItem('token');
        if(token){
            return true
        }
        else{
            this.$router.push({ name: 'login' });
        }
    },
    async logout(){
        const token = localStorage.getItem('token');
        const res = await axios.post('http://127.0.0.1:5000/logout',{
        },{
            headers: {
                'Authorization': 'Bearer ' + token
            }
        })
        localStorage.removeItem('token');
        this.$router.push({ name: 'login' });
    }

  },
  computed:{
    addNum(){
        return 1 + 2
    }
  },
  mounted(){
    this.fetchTasks()
    this.checkToken()
  }
}
</script>
