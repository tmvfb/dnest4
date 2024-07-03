#include "MyDistribution.h"
#include <cmath>

MyDistribution::MyDistribution()
{

}

void MyDistribution::from_prior(DNest4::RNG& rng)
{
	// Cauchy prior centered on 5.901 = log(365 days).
	// 0.97 and 0.485 account for truncation
	// tan()... denotes cauchy dist, check the link:
	// https://en.wikipedia.org/wiki/Cauchy_distribution
	// these all are Hyperparams defined in the paper

	center = 5.901 + tan(M_PI*(0.97*rng.rand() - 0.485));  // median orbital period
	width = 0.1 + 12.9*rng.rand();  // diversity of orbital periods
	mu = exp(tan(M_PI*(0.97*rng.rand() - 0.485)));  // mean amplitude (m/s), exp of Cauchy
}

double MyDistribution::perturb_hyperparameters(DNest4::RNG& rng)
{
	double logH = 0.;

	int which = rng.rand_int(3);

	if(which == 0)
	{
		// this just updates center with rand gauss noise
		center = (atan(center - 5.901)/M_PI + 0.485)/0.97;
		center += rng.randh();
		DNest4::wrap(center, 0., 1.);  // cuts the param (which is basically rng.rand()) if too big or small
		center = 5.901 + tan(M_PI*(0.97*center - 0.485));
	}
	else if(which == 1)
	{
		// this updates width with rand gauss noise
		width += 12.9*rng.randh();
		DNest4::wrap(width, 0.1, 13.);
	}
	else
	{
		// this updates semi-amplitude with rand gauss noise
		mu = log(mu);
		mu = (atan(mu)/M_PI + 0.485)/0.97;
		mu += rng.randh();
		DNest4::wrap(mu, 0., 1.);
		mu = tan(M_PI*(0.97*mu - 0.485));
		mu = exp(mu);
	}
	return logH;
}

// vec[0] = "position" (log-period)
// vec[1] = amplitude
// vec[2] = phase
// vec[3] = v0 - this is eccentrincity
// vec[4] = viewing angle
// these all are the planet params defined in the paper

double MyDistribution::log_pdf(const std::vector<double>& vec) const
{
	if(vec[1] < 0. ||
			vec[2] < 0. || vec[2] > 2.*M_PI ||
			vec[3] < 0. || vec[3] > 0.8189776 ||
			vec[4] < 0. || vec[4] > 2.*M_PI)
		return -1E300;

	return  -log(2.*width) - abs(vec[0] - center)/width  // log of biexponential for Pi (paper, footnote, page 4)
		-log(mu) - vec[1]/mu  // log of exponential for Ai (with param 1/mu for some reason)
		+ 2.1*log(1. - vec[3]/0.995);  // log of beta for eccentricity
	// other distributions are not present since they are constant???
}

void MyDistribution::from_uniform(std::vector<double>& vec) const
// this transforms some uniformly distributed parameter vectors
// to the desired distributions described in table 1
{
	if(vec[0] < 0.5)
		vec[0] = center + width*log(2.*vec[0]);
	else
		vec[0] = center - width*log(2. - 2.*vec[0]);
	vec[1] = -mu*log(1. - vec[1]);
	vec[2] = 2.*M_PI*vec[2];
	vec[3] = 1. - pow(1. - 0.995*vec[3], 1./3.1);
	vec[4] = 2.*M_PI*vec[4];
}

void MyDistribution::to_uniform(std::vector<double>& vec) const
{
	if(vec[0] < center)
		vec[0] = 0.5*exp((vec[0] - center)/width);
	else
		vec[0] = 1. - 0.5*exp((center - vec[0])/width);
	vec[1] = 1. - exp(-vec[1]/mu);
	vec[2] = vec[2]/(2.*M_PI);
	vec[3] = 1. - pow(1. - vec[3]/0.995, 3.1);
	vec[4] = vec[4]/(2.*M_PI);
}

void MyDistribution::print(std::ostream& out) const
{
	out<<center<<' '<<width<<' '<<mu<<' ';
}

