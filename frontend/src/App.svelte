<script>

    import Router from 'svelte-spa-router'
    import {push} from 'svelte-spa-router'
    import Login from "./Login.svelte";
    import {get} from 'svelte/store';
    import Register from "./Register.svelte";
    import TodoList from "./TodoList.svelte";
    import {token} from "./store";

    // configured urls
    const routes = {
        '/login': Login,
        '/register': Register,
        '/todos': TodoList,
    }

    let cur_token = get(token);

    if (cur_token === null) {
        // if user is not authorized
        // redirect to login page
        push('/login');
    }
    else {
        push('/todos');
    }


</script>

<main >
    <Router {routes}/>
</main>


