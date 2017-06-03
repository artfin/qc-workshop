/*
 Solution of the quantum harmonic oscillator
 Numerov algorithm
 Eigenvalue search using the shooting method
 Adimensional units:
 	X = (mK / hbar^2)^(1/4) X
	e = E / (hbar omega)
 */

#include <stdlib.h>
#include <stdio.h>
#include <math.h>

# define MSHX 2000 // Max numberof rid points

int main()
{
	double sqrt();

	int mesh, i, icl;

	int nodes, hnodes, ncross, parity, kkk, n_iter;

	double xmax, dx, ddx12, xmcl, norm, arg;

	double elw, eup, e;
	double *x, *y, *p, *vpot, *f;

	char fileout[80];
	FILE *out;

	// reading input data
	fprintf(stderr, 'Max value of x (typical value: 10):');
	scanf("%lf", &xmax);
	fprintf(stderr, "Number of grid points (typical value: 100):");
	scanf("%d", &mesh);

	// Allocating arrays (from 0 to mesh), grid initialization
	x = (double *) malloc((mesh + 1) * sizeof(double));
	y = (double *) malloc((mesh + 1) * sizeof(double));
	p = (double *) malloc((mesh + 1) * sizeof(double));
	f = (double *) malloc((mesh + 1) * sizeof(double));
	vpot = (double *) malloc((mesh + 1) * sizeof(double));
	
	dx = xmax / mesh;
	ddx12 = dx * dx / 12.0; // ?
		
	// setting up the potential (must be even w.r.t. x = 0)
	
	for (i = 0; i <= mesh; ++i) {
		x[i] = (double) i * dx;
		vpot[i] = 0.5 * x[i] * x[i];
	}

	fprintf(stderr, "Output file name = ");
	scanf("%80s", fileout);
	out = fopen(fileout, "w");

	// starting an eigenvalue search
	for (;;) {
		// Reading the number of nodes (stop if < 0)
		fprintf(stderr, "Number of nodes (-1 = exit): ");
		scanf("%d", &nodes);
		if (nodes < 0) {
			fclose(out);
			free(vpot);
			free(f);
			free(p);
			free(y);
			free(x);
			exit(0);
		}

		// setting initial lower and upper bounds to the eigenvalue
		eup = vpot[mesh]; // !!! 
		elw = eup; // !!!
		for (i = 0; i <= mesh; ++i) {
			if (vpot[i] < elw) {
				elw = vpot[i];
			}
			if (vpot[i] > eup) {
				eup = vpot[i];
			}
		}

		// setting trial energy
		fprintf(stderr, "Trial energy (0 = search with bisection):");
		scanf("%lf", &e);
		if (e == 0.) {
			// searching eigenvalues with bisection
			e = 0.5 * (elw + eup);
			n_iter = 1000;
		} else {
			// testing a single energy value
			n_iter = 1;
		}
			
		for (kkk = 0; (kkk < n_iter) && (eup - elw > 1e-10); kkk++) {
			// set up the f-function used by the Numerov algorithm
			// and determine the position of its last crossing, i.e. change of sign
			// f < 0 means classcally allowed region
			// f > 0 means classically forbidden region
			
			f[0] = ddx12 * (2.0 * (vpot[0] - e));
			icl = -1;
			for (i = 1; i <= mesh; ++i) {
				f[i] = ddx12 * 2.0 * (vpot[i] - e);

				// beware: if f[i] is exactly zero the change of sign is not observed. the following line is a trick to prevent missing a change of sign in this unlikely but not impossible case:
				if (f[i] == 0.0) {
					f[i] = 1e-20;
				}
				// store the index 'icl' where the last change of sign has been found 
				if (f[i] != copysign(f[i], f[i-1])) {
					icl = i;
				}
			}
			
			if (icl >= mesh - 2) {
				fprintf(stderr, "last change of sign too far.");
				exit(1);
			}

			if (icl < 1) {
				fprintf(stderr, "no classical turning point?");
				exit(1);
			}

			// f(x) as required by the Numerov algorithm
			for (i = 0; i <= mesh; ++i) {
				f[i] = 1.0 - f[i];
			}
			for (i = 0; i <= mesh; ++i) {
				y[i] = 0.0;
			}

			// determination of the wave-function in the first two points
			hnodes = nodes / 2;
			// beware of the integer division: 1/2 == 0 !
			// if number of nodes is even, there are 2 * hnodes nodes
			// if number of nodes is odd, there are 2 * hnodes + 1 nodes (one is in x = 0)
			// therefore, hnodes is the number of nodes in the x > 0 semi-axis (x = 0 excepted)
			
			if (2 * hnodes == nodes) {
				// even number of nodes: wf is even
				y[0] = 1.0;
				// assume f(-1) = f(1)
				y[1] = 0.5 * (12.0 - f[0] * 10.0) * y[0] / f[1];
			} else {
				// odd number of nodes: wf is odd
				y[0] = 0;
				y[1] = dx;
			}

			// outward integration and count number of crossings
			ncross = 0;
			for (i = 1; i <= mesh - 1; ++i) {
				y[i + 1] = ((12. - f[i] * 10.0) * y[i] - f[i - 1] * y[i - 1]) / f[i + 1];
				if (y[i] != copysign(y[i], y[i+1])) {
					++ncross;
				}
			}

			// check number of crossings
			
			fprintf(stdout, "%4d %4d %20.14f\n", kkk, ncross, e);
			if (n_iter > 1) {
				if (ncross > hnodes) {
					// too many crossings: current energy is too high
					// lower the upper bound
					eup = e;
				} else {
					// too few or correct number of crossings: current energy is too low
					// rase the lower bound
					elw = e;
				}
				// new trial value
				e = 0.5 * (eup + elw);
			}
		}
		// --- convergence has been achieved (or it wasn't required) ----
		// Note that the wavefunction is not normalized:
		// the problem is the divergence at large |x|
		//

		// Calculation of the classical probability density for energy e
		xmcl = sqrt(2.0 * e);
		norm = 0.0;
		for (i = icl; i <= mesh; ++i) {
			p[i] = 0.0;
		}
		for (i = 0; i <= icl - 1; ++i) { 
			arg = xmcl * xmcl - x[i] * x[i];
			if (arg > 0.0) {
				p[i] = 1.0 / sqrt(arg) / M_PI;
			} else {
				p[i] = 0;
			}
			norm += dx * 2 * p[i];
		}

		// the point at x = 0 must be counted once: 
		norm -= dx * p[0];
		// normalize p(x) so the Int p(x) dx = 1
		for (i = 0; i <= icl - 1; ++i) {
			p[i] /= norm;
		}
		// lines starting with # ignored by gnuplot
		fprintf(out, "# x    y(x)     y(x)^2     classical p(x) V\n");
// x < 0 region	
	}
}