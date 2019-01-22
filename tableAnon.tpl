<!DOCTYPE html>
<html>

<head>
	<title> Results </title>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
	<link rel="stylesheet" href="/static/style.css">
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
</head>

<div class="pull-right not_too_right">
	<div class="dropdown">
		<button class="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown">
			<div class="profilePic">
				<img src='https://d30y9cdsu7xlg0.cloudfront.net/png/29819-200.png' alt="Anonymous"></div>
			<span class="caret"></span>
		</button>
		<ul class="dropdown-menu dropdown-menu-right">
			<li><a href="#"> Hi Anonymous, </a></li>
			<li><a href="/login"> Log In</a></li>
		</ul>
	</div>
</div>

<body>
	<div class="container ">

		<div class="row h-100 justify-content-center align-items-center no-gutters">
			<div class="engineLogo">
				<img src="/static/beanlogo_animated.gif" style="width:17%;height:auto"; alt="Logo">
			</div>
		</div>

		<div class="row h-100 justify-content-center align-items-center">
				<form action="/search" method="post">
					<input class="form-control" name="keywords" placeholder="Search..." type="text" />
				</form>
				<div class="query-words">
					<form action="/">
						<input value="Back to Homepage" type="submit" class="btn btn-light" />
					</form>
				</div>
		</div>
		<div class="row h-100 justify-content-center align-items-center">
			<div class="history_table ">
				<h2> Search for "{{!keyword}}" </h2>
				{{!table}}
			</div>
		</div>
	</div>
</body>


</html>
