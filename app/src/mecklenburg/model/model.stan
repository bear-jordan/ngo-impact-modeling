data {
    int<lower=0> N;
    array[N] int<lower=0> alpha;
    array[N] int<lower=0> beta;
}
parameters {

}
generated quantities {
	array[N] real<lower=0, upper=1> theta;
	array[N] real<lower=0, upper=1> theta_null;

	for (n in 1:N) {
		theta_null[n] = bernoulli_rng(0.7);
	}
	theta = beta_rng(alpha, beta);
}
