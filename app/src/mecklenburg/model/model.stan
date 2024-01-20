data {
    int<lower=0> N;
    array[N] int<lower=0> alpha;
    array[N] int<lower=0> beta;
}
parameters {

}
generated quantities {
	array[N] real<lower=0, upper=1> theta;

	theta = beta_rng(alpha, beta);
}
