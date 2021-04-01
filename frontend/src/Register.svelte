<script>

	import {replace} from 'svelte-spa-router'
	import TodoList from "./TodoList.svelte";
	import Login from "./Login.svelte";

	let username;
	let password1;
	let password2;
	let text;

	async function sign_up () {
		let response = await fetch('http://127.0.0.1:8000/auth/users/',
				{
					method: "POST",
					body: JSON.stringify({
						'username': username,
						'password': password1
					}),
					headers: {
						"Content-Type": "application/json"
					}
				});

		const text = await response.text();
		if (response.ok) {
			await replace('/login')
			return text;
		}
		else {
			throw new Error(text);
		}
	}

	let result = sign_up();

	function handleClick(){
		if (password1 !== password2 ){
			throw new Error("passwords must be equal")
			// return "passwords must be equal"
			// todo: represent errors
		}
		else {
			result = sign_up();
		}
	}

	const routes = {
		'/login': Login,
		'/register': this,
		'/todos': TodoList,

	}

</script>


<main>


	<h1>Sign Up</h1>

	{#await result}
		<p>...waiting</p>
	{:then token}
		<p>{token}</p>
	{:catch error}
		<p style="color: red">{error.message}</p>
	{/await}

	<input required class="input-box" type="text" bind:value={username} placeholder="login"/>
	<input required class="input-box" type="password" bind:value={password1} placeholder="password"/>
	<input required class="input-box" type="password" bind:value={password2} placeholder="confirm password"/>
	<br>
	<a class="sign-in" href="#/login">Sign In</a>
	<br>
	<button class="signup-button" type="submit" on:click={handleClick}>Create account</button>

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

	.signup-button {
		background-color: #35b500;
		color: white;
		width: 200px;
		cursor: pointer;
	}
	.sign-in {
		color: green;
		padding-top: 20px;
	}
</style>