theoIntercept=-26.406
intersection=1475

#files name
fileName<-c("PtSlab111Z_6E_1.dat","PtSlab111Z_6E_2.dat","PtSlab111Z_6E_3.dat","PtSlab111Z_6E_4.dat")

#varibale defination

#number of diffirent fields
nE=4

#number of different k
nk=6

#total atoms
N=9000

#calculation of E
	    
	    
	    
	    
E<-seq(1,4)*0.1*1e10
#E<-log(Ef,10)
#E<-Ef

n=length(fileName)
pz<-matrix(seq(1,nE*nk),nrow=nE,ncol=nk)
err<-matrix(seq(1,nE*nk),nrow=nE,ncol=nk)
for(j in seq(1,nk)){
	for( i in seq(1,nE)){
		data<-read.table(fileName[i])
		pz[i,j]<-data$V2[j]
		err[i,j]<-data$V3[j]

	#	pz[i,j]<-data$V2[j]
	#	err[i,j]<-data$V3[j]
	}
}
count<-1:nk
k<-seq(6,17,2)
int<-1:nk
alpha<-1:nk
ealpha<-1:nk
slo<-1:nk
eint<-1:nk
eslo<-1:nk
for (var in count){


	#file<-paste(as.character((var+1)*100),"k.pdf") #unweighted
	file<-paste(as.character((var+1)*100),"k_W.pdf")    #weighted
	p<-pz[,var]
	er<-err[,var]
	#fit<-lm(p~E)						#unweighted
	fit<-lm(p~E,weights=1/er)				#weighted fit where weight is 1/err
	summ<-summary(fit)
	int[var]<-(summ$coef[1,1])
	slo[var]<-(summ$coef[2,1])
	alpha[var]<-(slo[var]/8.854e-12)*N*1e30
	eint[var]<-(summ$coef[1,2])
	eslo[var]<-(summ$coef[2,2])
	ealpha[var]<-eslo[var]*N*1e30/8.854e-12
	erroralpha<-as.character(ealpha)
	errorIntercept<-as.character(eint)
	intercept<-as.character(summ$coef[1,1])
	Alpha<-as.character(alpha)
	info<-c(intercept,Alpha)
	errInfo<-c(errorIntercept,erroralpha)

	subtitle<-paste(info,collapse=" = intercept ||  slope = ")
	title<-paste(errInfo,collapse=" = eint || eslo = ")
	pdf(file)

#	plot(E,p,main=paste("k = ",as.character((var+1)*100)),xlab=expression(log(E,10)),ylab=expression(log(p_z,10)),sub=subtitle)
	plot(E,p,main=title,xlab=expression(E),ylab=expression(p_z),sub=subtitle)

	abline(fit)
	arrows(E, p-er, E, p+er, length=0.05, angle=90, code=3)
	dev.off()

}


k<-k*100
fit<-smooth.spline(k,alpha,all.knots=T)
#pdf("best_intercept.pdf")			#unweighted
pdf("best_intercept_wt.pdf")			#weighted


plot(k,alpha,xlab="K",ylab=expression(alpha),main="K vrs slope for Pt100_6L",sub=paste("Approx value of k=", as.character(intersection)))
lines(fit,lty=3)
arrows(k,alpha-ealpha,k,alpha+ealpha,length=0.05,angle=90,code=3)
#abline(theoIntercept,0,lwd=2)
#abline(v=1100,h=0,lty=4)
#abline(v=1300,h=0,lty=4)
#abline(v=intersection,h=0,lty=4)
dev.off()
#summary(fit)

dataTable<-list("k"=k,"alpha"=alpha,"Delta_alpha"=ealpha,"int"=int,"Delta_int"=eint)
#write.table(dataTable,"Pt_K_vrs_log(alpha).dat")	#unweighted
write.table(dataTable,"Pt_K_vrs_log(alpha)_wt.dat")   #weighted
