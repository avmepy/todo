<script>

	import Login from "./Login.svelte";
	import Register from "./Register.svelte";
	import { get} from 'svelte/store';
	import {token} from "./store";
	import {replace} from "svelte-spa-router";

	let new_text_todo;
	let new_text_subtask;
	$: new_color_todo = '#dcdcdc';
	let id_todo_add_subtask;
	let addingSubtask = false;
	let addingTodo = false;

	let cur_token = get(token);

	if (cur_token === null) {
		replace('/login')
	}

	async function logout () {

		let response = await fetch('http://127.0.0.1:8000/auth/token/logout/',
				{
					method: "POST",
					headers: {
						"Authorization": 'Token '+ cur_token,
						"Content-Type": "application/json"
					}
				});

		const todos = await response.json();
		if (response.ok) {
			cur_token = null;
			return todos;
		}

		else {
			throw new Error(response.statusText);
		}
	}

	function fAddSubTask(todo_id) {
		addingSubtask = true;
		id_todo_add_subtask = todo_id;

	}

	function  fCancelingSubTask () {
		addingSubtask = false;
	}

	function fAddTodo () {
		addingTodo = true;
	}

	function fCancelingTodo () {
		addingTodo = false;
	}


	async function get_todos() {
		let response = await fetch('http://127.0.0.1:8000/api/todos/',
				{
					method: "GET",
					headers: {
						"Authorization": 'Token '+ cur_token,
						"Content-Type": "application/json"
					}
				});

		const todos = await response.json();
		if (response.ok) {
			return todos;
		}

		else {
			throw new Error(response.statusText);
		}
	}


	let result = get_todos();

	const routes = {
		'/login': Login,
		'/register': Register,
		'/todos': this,

	}


	async function addTodo () {


		let response = await fetch('http://127.0.0.1:8000/api/todos/',
				{
					method: "POST",
					body: JSON.stringify({
						'text': new_text_todo,
						'color': new_color_todo,
					}),
					headers: {
						"Authorization": 'Token ' + cur_token,
						"Content-Type": "application/json"
					}
				});

		const text = await response.text();
		if (response.ok) {
			// await result = get_todos()
			return text;
		}

		else {
			throw new Error(text);
		}

	}

	async function removeTodo (cur_id) {

		let response = await fetch('http://127.0.0.1:8000/api/todos/' + cur_id + '/',
				{
					method: "DELETE",
					headers: {
						"Authorization": 'Token '+ cur_token,
						"Content-Type": "application/json"
					}
				});

		const text = await response.text();
		if (response.ok) {
			// await result = get_todos()
			return text;
		}

		else {
			throw new Error(text);
		}

	}

	async function addSubTask (todo_id) {
		let response = await fetch('http://127.0.0.1:8000/api/subtasks/',
				{
					method: "POST",
					body: JSON.stringify({
						'text': new_text_subtask,
						'todo_id': todo_id,
					}),
					headers: {
						"Authorization": 'Token ' + cur_token,
						"Content-Type": "application/json"
					}
				});

		const text = await response.text();
		if (response.ok) {
			// await result = get_todos()
			return text;
		}

		else {
			throw new Error(text);
		}

	}


	async function removeSubTask (cur_id, cur_todo) {

		let response = await fetch('http://127.0.0.1:8000/api/subtasks/' + cur_id + '/',
				{
					method: "DELETE",
					body: JSON.stringify({
						'todo_id': cur_todo,

					}),
					headers: {
						"Authorization": 'Token '+ cur_token,
						"Content-Type": "application/json"
					}
				});

		const text = await response.text();
		if (response.ok) {
			// await result = get_todos()
			return text;
		}

		else {
			throw new Error(text);
		}

	}


</script>

<main>

	<div class="jc-space-between">
		<button class="green-button" on:click={fAddTodo}>add TODO</button>
		<div>
			<span>hello: </span>
			<button class="logout" on:click={logout}>logout</button>
		</div>
	</div>
	<hr class="hr">

	{#if addingTodo}
		<div class="add-todo-box" style="border-color: {new_color_todo}">

			<input type="text" class="input-todo-text" placeholder="some text..."
				   bind:value={new_text_todo}>
			<div class="display-flex">
				<div class="colors">
					<div class="choose-color bcolor-blue margin-lr-3" on:click={() => {new_color_todo = '#6fa8dc'}}></div>
					<div class="choose-color bcolor-green margin-lr-3" on:click={() => {new_color_todo='#6aa84f'}}></div>
					<div class="choose-color bcolor-yellow margin-lr-3" on:click={() => {new_color_todo='#fbce9c'}}></div>
				</div>
				<button class="green-button" on:click={addTodo}>save</button>
				<button class="white-button" on:click={fCancelingTodo}>cancel</button>
			</div>
		</div>
	{/if}

	<p class="text-align-start">added TODO</p>

	<div class="scroll">
		{#await result}
			<p>Loading...</p>
		{:then todos}
			{#each todos as todo}
				<div class="todo" style="background-color: {todo.color}">
					<svg on:click={() => fAddSubTask(todo.id)} mlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-circle" viewBox="0 0 16 16">
						<path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
						<path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
					</svg>
					<span>{todo.text}</span>
					<button on:click={removeTodo} class="remove-button" on:click={() => removeTodo(todo.id)}>remove</button>
				</div>

				<div>
					{#if addingSubtask && todo.id === id_todo_add_subtask}
						<div class="subtask margin-left-100">
							<input type="text" class="input-todo-text" placeholder="some text..." bind:value={new_text_subtask}>
							<button class="green-button" on:click={() => {addSubTask(todo.id)}}>save</button>
							<button class="white-button" on:click={fCancelingSubTask}>cancel</button>
						</div>
					{/if}
					{#each todo.subtasks as subtask}

						<div class="subtask margin-left-100">
							<div>{subtask.text}</div>
							<button class="remove-button" on:click={() => removeSubTask(subtask.id, todo.id)}>remove</button>
						</div>

					{/each}
				</div>
			{/each}
		{:catch error}
			<p style="color: #ff0000">{error.message}</p>
		{/await}
	</div>
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

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
	.relative {
		position: relative;
	}
	.absolute {
		position: absolute;
	}
	.right-0{
		right: 0;
	}
	.margin-left-100{
		margin-left: 100px;
	}
	.text-align-start {
		text-align: start;
	}
	.text-align-end {
		text-align: end;
	}

	.bcolor-yellow {
		background-color: #fbce9c;
	}
	.bcolor-blue {
		background-color: #6fa8dc;
	}
	.bcolor-green {
		background-color: #6aa84f;
	}
	.remove-button {
		background-color: #ea1e00;
		color: white;
		border-radius: 10px;
		height: 30px;
	}
	.margin-lr-3 {
		margin: 0 3px;
	}

	button {
		margin: 0;
	}

	.todo {
		justify-content: space-between;
		width: 500px;
		border: 3px #d0d0d0 solid;
		border-radius: 10px;
		margin-bottom: 10px;
		display: flex;
		align-items: center;
	}

	.jc-space-between{
		justify-content: space-around;
		display: flex;
	}

	.green-button {
		background-color: #35b500;
		color: white;
		border-radius: 10px;
		cursor: pointer;
	}
	.white-button {
		background-color: #ffffff;
		color: black;
		border-radius: 10px;
		cursor: pointer;
	}

	.logout {
		background: #999999;
		color: #ffffff;
		border-radius: 10px;
	}

	.hr {
		/*margin: 10px 0;*/
		color: black;
		border: 1px solid;
	}

	.add-todo-box {
		justify-content: space-between;
		width: 500px;
		border: 3px #d0d0d0 solid;
		border-radius: 10px;
		margin-bottom: 10px;
		display: flex;
		align-items: center;
		height: 50px;
	}
	.input-todo-text {
		border: black solid;
		margin: 0;
	}

	.choose-color {
		border-radius: 100%;
		width: 20px;
		height: 20px;
		cursor: pointer;
	}
	.colors {
		display: flex;
	}
	.display-flex {
		display: flex;
		align-items: center;
	}
	.subtask {
		justify-content: space-between;
		width: 400px;
		border: 3px #000000 solid;
		border-radius: 10px;
		margin-bottom: 10px;
		display: flex;
		align-items: center;
		height: 50px;
		background: #e9e9e9;
	}
	.scroll {
		height: 500px;
		overflow-y: auto;
		border: solid lightgray 1px;
		border-radius: 10px;
		padding: 15px;
	}
</style>
