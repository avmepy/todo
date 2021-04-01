<script>

	import {get} from 'svelte/store';
	import {token} from './store.js';
	import {replace} from 'svelte-spa-router'
	import Register from "./Register.svelte";
	import TodoList from "./TodoList.svelte";

	let username;
	let password;

	let cur_token = get(token);
	if (cur_token !== null) {
		//redirecting to todos if already logged in
		replace('/todos')
	}

	export async function sign_in() {
		let response = await fetch('http://127.0.0.1:8000/auth/token/login/',
				{
					method: "POST",
					body: JSON.stringify({
						'username': username,
						'password': password
					}),
					headers: {
						"Content-Type": "application/json"
					}
				});

		const text = await response.text();
		// couldn't get token with .json() method
		// todo: remake redo from json
		// todo: cookie
		// const res = await response.json();
		if (response.ok) {
			// setContext('token', text.split('"')[3]);
			await token.set(text.split('"')[3]);
			await replace('/todos')

		}
		else {
			throw new Error(text);
		}
	}

	let result = sign_in();

	function handleClick(){
		result = sign_in();
	}

	const routes = {
		'/login': this,
		'/register': Register,
		'/todos': TodoList,
	}

</script>

<main>
	<h1>Login page</h1>

	{#await result}
		<p>...waiting</p>
	{:then token}
		<p>Welcome</p>
	{:catch error}
		<p style="color: red">Something went wrong. Please try again {error.message}</p>
	{/await}

	<input required class="input-box" type="text" bind:value={username} placeholder="login"/>
	<input required class="input-box" type="password" bind:value={password} placeholder="password"/>
	<br>
	<div><a class="sign-up" href="#/register">Sign Up</a></div>
	<button class="login-button" on:click={handleClick}>enter</button>

</main>

<style>
	main {
		text-align: center;
		/*display: flex;*/
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
		display: table;
	}

	.input-box {
		border: black solid;
		width: 200px;
		height: 30px;
		margin: 5px 0;
	}

	.login-button {
		background-color: #35b500;
		color: white;
		width: 200px;
		cursor: pointer;
	}
	.sign-up {
		color: green;
		padding-top: 20px;
	}
</style>