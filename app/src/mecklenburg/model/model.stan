data {
    int<lower=0> N;
    array[N] int<lower=0> alpha;
    array[N] int<lower=0> beta;
}
parameters {

}
generated quantities {
	array[N] real<lower=0, upper=1> theta;
	array[N] int<lower=0, upper=1> y_sim;

	array[N] real<lower=0, upper=1> theta_null;
	array[N] int<lower=0, upper=1> y_null_sim;

	for (n in 1:N) {
		theta[n] = beta_rng(alpha[n], beta[n]);
		theta_null[n] = bernoulli_rng(0.7);

		y_sim[n] = bernoulli_rng(theta[n]);
		y_null_sim[n] = bernoulli_rng(theta_null[n]);
	}
}
