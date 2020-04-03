#include <stdio.h>
#include <stdlib.h>
#include<math.h>

#include"mex.h"
#define M_PI  3.14159265358979323846
#define RADIANS_TO_DEGREES (180.0/M_PI)
int max(int x, int y)
{
   if(x<y)
      return y;
   else
      return x;
}
int min(int x, int y)
{
   return x<y?x:y;
}
void mexFunction(int nlhs,mxArray *plhs[],int nrhs,const mxArray *prhs[])
{
   double * image;
   int x,y,i,j,n,k;
   double ax,ay,an,ap;
   int X;  /* x image size */
   int Y;  /* y image size */
   double *p_alpha;
   double beta;
  
   image=mxGetPr(prhs[0]);
   p_alpha=mxGetPr(prhs[1]);
   beta=p_alpha[0];
   X=mxGetM(prhs[0]);
   Y=mxGetN(prhs[0]);
 
   double * gradx;
   double * grady;
   int imgSize=X*Y;
   double *img1;
   img1= (double *) malloc( X * Y * sizeof(double) );
   double *img2;
   img2= (double *) malloc( X * Y * sizeof(double) );

   for(i=0;i<imgSize;i++)
   {
      img1[i]=image[i];
      if(img1[i]<1.)
         img2[i]=1.;
      else
         img2[i]=img1[i];
   }
   int longueur=ceil(log(10)*beta);
   int largeur=longueur;
   double * gradx1;
   gradx1= (double *) malloc( X * Y * sizeof(double) );
   double * grady1;
   grady1= (double *) malloc( X * Y * sizeof(double) );
   for(j=0;j<Y;j++)
   {
      for(i=0;i<X;i++)
      {
         double Mx=0;
         double My=0;
         for(k=-largeur;k<=largeur;k++)
         {
            int xk=min(max(i+k,0),X-1);
            int yk=min(max(j+k,0),Y-1);
            double coeff=exp(-(double) abs(k)/beta);
            Mx+=coeff*img2[xk+j*X];
            My+=coeff*img2[i+yk*X];    
         }
         gradx1[i+j*X]=Mx;
         grady1[i+j*X]=My;
      }
   }

   double * gradn;
   double * gradp;
   plhs[0]=mxCreateDoubleMatrix(X,Y,mxREAL);
   plhs[1]=mxCreateDoubleMatrix(X,Y,mxREAL);
   plhs[2]=mxCreateDoubleMatrix(X,Y,mxREAL);
   plhs[3]=mxCreateDoubleMatrix(X,Y,mxREAL);
   gradn=mxGetPr(plhs[0]);
   gradp=mxGetPr(plhs[1]);
   gradx=mxGetPr(plhs[2]);
   grady=mxGetPr(plhs[3]);
   for(j=0;j<Y;j++)
   {
      for(i=0;i<X;i++)
      {
         double Mxg=0;
         double Mxd=0;
         double Myg=0;
         double Myd=0;
         for(k=0;k<=longueur;k++)
         {
            double coeff=exp(-(double) abs(k)/beta);
            int yl1;
            if(j-k<0)
               yl1=0;
            else
               yl1=j-k;
            int yl2;
            if(j+k>Y-1)
               yl2=Y-1;
            else
               yl2=j+k;
            Mxg+=coeff*gradx1[i+yl1*X];
            Mxd+=coeff*gradx1[i+yl2*X];
            int xl1=max(i-k,0);
            int xl2=min(i+k,X-1);;
            Myg+=coeff*grady1[xl1+j*X];
            Myd+=coeff*grady1[xl2+j*X];
         }
         gradx[i+j*X]=log(Mxd/Mxg);
         grady[i+j*X]=log(Myd/Myg);
      }
   }

   for(i=0;i<imgSize;i++)
   {
      ay=gradx[i];
      ax=grady[i];
      ap=atan2((double) ax,(double) ay);
      gradp[i]=ap;
      an=(double) hypot((double) ax,(double) ay);
      gradn[i]=an;
   }
   if( image == NULL )
   {
      fprintf(stderr,"error: not enough memory\n");
      exit(EXIT_FAILURE);
   }
   free((void *) img1);
   free((void *) img2);
   free((void *) gradx1);
   free((void *) grady1);
}
