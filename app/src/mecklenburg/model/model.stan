data {
    int<lower=0> N;
    vector<lower=0>[N] alpha_raw;
    vector<lower=0>[N] beta_raw;
}
transformed data {
    vector<lower=0>[N] alpha;
    vector<lower=0>[N] beta;
	
	alpha = alpha_raw + 0.01;
	beta = beta_raw + 0.01;
}
generated quantities {
	array[N] real<lower=0, upper=1> theta;
	array[N] int<lower=0, upper=1> y_sim;

	theta = beta_rng(alpha, beta);
	y_sim = bernoulli_rng(theta);
}
