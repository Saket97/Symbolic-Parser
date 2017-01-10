#include <stdio.h>
#include <stdlib.h>
#include <string.h>
char s[30][10]; //same dimension as s in line 1236
int pos;
int map(char*s){
	if (strcmp(s,"|") == 0)
	return 0;
	else
	if (strcmp(s,"&") == 0)
	return 1;
	else
	if (strcmp(s,"+") == 0)
	return 2;
	else
	if (strcmp(s,"-") == 0)
	return 3;
	else
	if (strcmp(s,"*") == 0)
	return 4;
	else
	if (strcmp(s,"/") == 0)
	return 5;
	else
	if (strcmp(s,"nil") == 0)
	return 6;
	else
	if (strcmp(s,"integer") == 0)
	return 7;
	else
	if (strcmp(s,"string") == 0)
	return 8;
	else
	if (strcmp(s,"(") == 0)
	return 9;
	else
	if (strcmp(s,")") == 0)
	return 10;
	else
	if (strcmp(s,"if") == 0)
	return 11;
	else
	if (strcmp(s,"then") == 0)
	return 12;
	else
	if (strcmp(s,"else") == 0)
	return 13;
	else
	if (strcmp(s,"while") == 0)
	return 14;
	else
	if (strcmp(s,"do") == 0)
	return 15;
	else
	if (strcmp(s,"for") == 0)
	return 16;
	else
	if (strcmp(s,"id") == 0)
	return 17;
	else
	if (strcmp(s,":=") == 0)
	return 18;
	else
	if (strcmp(s,"to") == 0)
	return 19;
	else
	if (strcmp(s,"break") == 0)
	return 20;
	else
	if (strcmp(s,"let") == 0)
	return 21;
	else
	if (strcmp(s,"in") == 0)
	return 22;
	else
	if (strcmp(s,"end") == 0)
	return 23;
	else
	if (strcmp(s,"type") == 0)
	return 24;
	else
	if (strcmp(s,"=") == 0)
	return 25;
	else
	if (strcmp(s,"{") == 0)
	return 26;
	else
	if (strcmp(s,"}") == 0)
	return 27;
	else
	if (strcmp(s,"array") == 0)
	return 28;
	else
	if (strcmp(s,"of") == 0)
	return 29;
	else
	if (strcmp(s,":") == 0)
	return 30;
	else
	if (strcmp(s,",") == 0)
	return 31;
	else
	if (strcmp(s,"var") == 0)
	return 32;
	else
	if (strcmp(s,"function") == 0)
	return 33;
	else
	if (strcmp(s,"[") == 0)
	return 34;
	else
	if (strcmp(s,"]") == 0)
	return 35;
	else
	if (strcmp(s,".") == 0)
	return 36;
	else
	if (strcmp(s,";") == 0)
	return 37;
	else
	if (strcmp(s,"!=") == 0)
	return 38;
	else
	if (strcmp(s,">") == 0)
	return 39;
	else
	if (strcmp(s,"<") == 0)
	return 40;
	else
	if (strcmp(s,">=") == 0)
	return 41;
	else
	if (strcmp(s,"<=") == 0)
	return 42;
	else
	if (strcmp(s,"dol") == 0)
	return 43;
}
void Prog();
void Exp();
void ExpOR();
void ExpORPr();
void ExpANDPr();
void ExpAND();
void ArithExp();
void RelationExp();
void Term();
void TermPr();
void FactorPr();
void Factor();
void IF_extra();
void DecList();
void DL_extra();
void Dec();
void TyDec();
void Ty();
void FieldList();
void FL_extra();
void FieldExpList();
void FEL_extra();
void TypeId();
void VD_extra();
void VarDec();
void FunDec();
void LValue();
void LD_extra();
void FunctionRecordArray();
void FRA_extra();
void FRA_extra1();
void FRAP_extra1();
void FunctionRecordArrayPr();
void FRAP_extra();
void ExpList();
void EL_extra();
void ArgList();
void AL_extra();
void UnaryOp();
void RelationOp();
void consume_token(int val)
{
	if (val == map(s[pos]))
	pos += 1;
	else
	{
		printf("Error...!\n");
		exit(1);
	}	
}void Prog(){
	//printf("Prog %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d Prog\n",pos);
		exit(1);
		case 9:
		case 8:
		case 20:
		case 7:
		case 14:
		case 17:
		case 11:
		case 16:
		case 3:
		case 6:
		case 21:
		Exp();
		break;
	}
}
void Exp(){
	//printf("Exp %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d Exp\n",pos);
		exit(1);
		case 9:
		case 8:
		case 20:
		case 7:
		case 14:
		case 17:
		case 11:
		case 16:
		case 3:
		case 6:
		case 21:
		ExpOR();
		ExpORPr();
		break;
	}
}
void ExpOR(){
	//printf("ExpOR %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d ExpOR\n",pos);
		exit(1);
		case 9:
		case 8:
		case 20:
		case 7:
		case 14:
		case 17:
		case 11:
		case 16:
		case 3:
		case 6:
		case 21:
		ExpAND();
		ExpANDPr();
		break;
	}
}
void ExpORPr(){
	//printf("ExpORPr %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d ExpORPr\n",pos);
		exit(1);
		case 0:
		consume_token(map("|"));
		Exp();
		break;
		case 41:
		case 38:
		case 1:
		case 4:
		case 31:
		case 19:
		case 32:
		case 24:
		case 40:
		case 39:
		case 33:
		case 15:
		case 13:
		case 12:
		case 42:
		case 22:
		case 23:
		case 10:
		case 2:
		case 3:
		case 5:
		case 37:
		case 25:
		case 35:
		case 43:
		case 27:
		break;
	}
}
void ExpANDPr(){
	//printf("ExpANDPr %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d ExpANDPr\n",pos);
		exit(1);
		case 1:
		consume_token(map("&"));
		ExpOR();
		break;
		case 41:
		case 38:
		case 4:
		case 31:
		case 19:
		case 32:
		case 24:
		case 40:
		case 39:
		case 33:
		case 15:
		case 13:
		case 0:
		case 12:
		case 42:
		case 22:
		case 23:
		case 10:
		case 2:
		case 3:
		case 5:
		case 37:
		case 25:
		case 35:
		case 43:
		case 27:
		break;
	}
}
void ExpAND(){
	//printf("ExpAND %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d ExpAND\n",pos);
		exit(1);
		case 9:
		case 8:
		case 20:
		case 7:
		case 14:
		case 17:
		case 11:
		case 16:
		case 3:
		case 6:
		case 21:
		ArithExp();
		RelationExp();
		break;
	}
}
void ArithExp(){
	//printf("ArithExp %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d ArithExp\n",pos);
		exit(1);
		case 9:
		case 8:
		case 20:
		case 7:
		case 14:
		case 17:
		case 11:
		case 16:
		case 3:
		case 6:
		case 21:
		Term();
		TermPr();
		break;
	}
}
void RelationExp(){
	//printf("RelationExp %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d RelationExp\n",pos);
		exit(1);
		case 41:
		case 38:
		case 40:
		case 39:
		case 42:
		case 25:
		RelationOp();
		ArithExp();
		break;
		case 1:
		case 4:
		case 31:
		case 19:
		case 32:
		case 24:
		case 33:
		case 15:
		case 13:
		case 0:
		case 12:
		case 22:
		case 23:
		case 10:
		case 2:
		case 3:
		case 5:
		case 37:
		case 35:
		case 43:
		case 27:
		break;
	}
}
void Term(){
	//printf("Term %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d Term\n",pos);
		exit(1);
		case 9:
		case 8:
		case 20:
		case 7:
		case 14:
		case 17:
		case 11:
		case 16:
		case 3:
		case 6:
		case 21:
		Factor();
		FactorPr();
		break;
	}
}
void TermPr(){
	//printf("TermPr %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d TermPr\n",pos);
		exit(1);
		case 2:
		consume_token(map("+"));
		Term();
		TermPr();
		break;
		case 3:
		consume_token(map("-"));
		Term();
		TermPr();
		break;
		case 41:
		case 38:
		case 1:
		case 4:
		case 31:
		case 19:
		case 32:
		case 24:
		case 40:
		case 39:
		case 33:
		case 15:
		case 13:
		case 0:
		case 12:
		case 42:
		case 22:
		case 23:
		case 10:
		case 5:
		case 37:
		case 25:
		case 35:
		case 43:
		case 27:
		break;
	}
}
void FactorPr(){
	//printf("FactorPr %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d FactorPr\n",pos);
		exit(1);
		case 4:
		consume_token(map("*"));
		Factor();
		FactorPr();
		break;
		case 41:
		case 38:
		case 1:
		case 31:
		case 19:
		case 32:
		case 24:
		case 40:
		case 39:
		case 33:
		case 15:
		case 13:
		case 0:
		case 12:
		case 42:
		case 22:
		case 23:
		case 10:
		case 2:
		case 3:
		case 37:
		case 25:
		case 35:
		case 43:
		case 27:
		break;
		case 5:
		consume_token(map("/"));
		Factor();
		FactorPr();
		break;
	}
}
void Factor(){
	//printf("Factor %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d Factor\n",pos);
		exit(1);
		case 6:
		consume_token(map("nil"));
		break;
		case 7:
		consume_token(map("integer"));
		break;
		case 8:
		consume_token(map("string"));
		break;
		case 9:
		consume_token(map("("));
		ExpList();
		consume_token(map(")"));
		break;
		case 3:
		UnaryOp();
		Exp();
		break;
		case 11:
		consume_token(map("if"));
		Exp();
		consume_token(map("then"));
		Exp();
		IF_extra();
		break;
		case 14:
		consume_token(map("while"));
		Exp();
		consume_token(map("do"));
		Exp();
		break;
		case 16:
		consume_token(map("for"));
		consume_token(map("id"));
		consume_token(map(":="));
		Exp();
		consume_token(map("to"));
		Exp();
		consume_token(map("do"));
		Exp();
		break;
		case 20:
		consume_token(map("break"));
		break;
		case 21:
		consume_token(map("let"));
		DecList();
		consume_token(map("in"));
		ExpList();
		consume_token(map("end"));
		break;
		case 17:
		LValue();
		break;
	}
}
void IF_extra(){
	//printf("IF_extra %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d IF_extra\n",pos);
		exit(1);
		case 13:
		consume_token(map("else"));
		Exp();
		break;
		case 41:
		case 38:
		case 1:
		case 4:
		case 31:
		case 19:
		case 32:
		case 24:
		case 40:
		case 39:
		case 33:
		case 15:
		case 0:
		case 12:
		case 42:
		case 22:
		case 23:
		case 10:
		case 2:
		case 3:
		case 5:
		case 37:
		case 25:
		case 35:
		case 43:
		case 27:
		break;
	}
}
void DecList(){
	//printf("DecList %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d DecList\n",pos);
		exit(1);
		case 32:
		case 24:
		case 33:
		case 22:
		DL_extra();
		break;
	}
}
void DL_extra(){
	//printf("DL_extra %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d DL_extra\n",pos);
		exit(1);
		case 32:
		case 24:
		case 33:
		Dec();
		DL_extra();
		break;
		case 22:
		break;
	}
}
void Dec(){
	//printf("Dec %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d Dec\n",pos);
		exit(1);
		case 24:
		TyDec();
		break;
		case 32:
		VarDec();
		break;
		case 33:
		FunDec();
		break;
	}
}
void TyDec(){
	//printf("TyDec %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d TyDec\n",pos);
		exit(1);
		case 24:
		consume_token(map("type"));
		TypeId();
		consume_token(map("="));
		Ty();
		break;
	}
}
void Ty(){
	//printf("Ty %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d Ty\n",pos);
		exit(1);
		case 28:
		consume_token(map("array"));
		consume_token(map("of"));
		TypeId();
		break;
		case 26:
		consume_token(map("{"));
		FieldList();
		consume_token(map("}"));
		break;
		case 8:
		case 7:
		case 17:
		TypeId();
		break;
	}
}
void FieldList(){
	//printf("FieldList %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d FieldList\n",pos);
		exit(1);
		case 10:
		case 27:
		break;
		case 17:
		consume_token(map("id"));
		consume_token(map(":"));
		TypeId();
		FL_extra();
		break;
	}
}
void FL_extra(){
	//printf("FL_extra %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d FL_extra\n",pos);
		exit(1);
		case 31:
		consume_token(map(","));
		consume_token(map("id"));
		consume_token(map(":"));
		TypeId();
		FL_extra();
		break;
		case 10:
		case 27:
		break;
	}
}
void FieldExpList(){
	//printf("FieldExpList %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d FieldExpList\n",pos);
		exit(1);
		case 17:
		consume_token(map("id"));
		consume_token(map("="));
		Exp();
		FEL_extra();
		break;
	}
}
void FEL_extra(){
	//printf("FEL_extra %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d FEL_extra\n",pos);
		exit(1);
		case 31:
		consume_token(map(","));
		consume_token(map("id"));
		consume_token(map("="));
		Exp();
		FEL_extra();
		break;
	}
}
void TypeId(){
	//printf("TypeId %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d TypeId\n",pos);
		exit(1);
		case 17:
		consume_token(map("id"));
		break;
		case 7:
		consume_token(map("integer"));
		break;
		case 8:
		consume_token(map("string"));
		break;
	}
}
void VD_extra(){
	//printf("VD_extra %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d VD_extra\n",pos);
		exit(1);
		case 18:
		case 25:
		break;
		case 30:
		consume_token(map(":"));
		TypeId();
		break;
	}
}
void VarDec(){
	//printf("VarDec %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d VarDec\n",pos);
		exit(1);
		case 32:
		consume_token(map("var"));
		consume_token(map("id"));
		VD_extra();
		consume_token(map(":="));
		Exp();
		break;
	}
}
void FunDec(){
	//printf("FunDec %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d FunDec\n",pos);
		exit(1);
		case 33:
		consume_token(map("function"));
		consume_token(map("id"));
		consume_token(map("("));
		FieldList();
		consume_token(map(")"));
		VD_extra();
		consume_token(map("="));
		Exp();
		break;
	}
}
void LValue(){
	//printf("LValue %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d LValue\n",pos);
		exit(1);
		case 17:
		consume_token(map("id"));
		LD_extra();
		break;
	}
}
void LD_extra(){
	//printf("LD_extra %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d LD_extra\n",pos);
		exit(1);
		case 41:
		case 18:
		case 38:
		case 1:
		case 4:
		case 31:
		case 36:
		case 19:
		case 32:
		case 24:
		case 40:
		case 39:
		case 33:
		case 15:
		case 13:
		case 0:
		case 12:
		case 42:
		case 22:
		case 23:
		case 10:
		case 2:
		case 3:
		case 5:
		case 37:
		case 25:
		case 35:
		case 43:
		case 27:
		FunctionRecordArrayPr();
		break;
		case 9:
		case 34:
		case 26:
		FunctionRecordArray();
		break;
	}
}
void FunctionRecordArray(){
	//printf("FunctionRecordArray %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d FunctionRecordArray\n",pos);
		exit(1);
		case 34:
		consume_token(map("["));
		Exp();
		consume_token(map("]"));
		FRA_extra1();
		break;
		case 9:
		consume_token(map("("));
		ArgList();
		consume_token(map(")"));
		break;
		case 26:
		consume_token(map("{"));
		consume_token(map("id"));
		consume_token(map("="));
		Exp();
		FRA_extra();
		consume_token(map("}"));
		break;
	}
}
void FRA_extra(){
	//printf("FRA_extra %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d FRA_extra\n",pos);
		exit(1);
		case 31:
		consume_token(map(","));
		consume_token(map("id"));
		consume_token(map("="));
		Exp();
		FRA_extra();
		break;
		case 27:
		break;
	}
}
void FRA_extra1(){
	//printf("FRA_extra1 %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d FRA_extra1\n",pos);
		exit(1);
		case 41:
		case 18:
		case 38:
		case 1:
		case 4:
		case 31:
		case 36:
		case 19:
		case 32:
		case 24:
		case 40:
		case 39:
		case 33:
		case 15:
		case 13:
		case 0:
		case 12:
		case 42:
		case 22:
		case 23:
		case 10:
		case 2:
		case 3:
		case 5:
		case 37:
		case 25:
		case 34:
		case 35:
		case 43:
		case 27:
		FunctionRecordArrayPr();
		break;
		case 29:
		consume_token(map("of"));
		Exp();
		break;
	}
}
void FRAP_extra1(){
	//printf("FRAP_extra1 %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d FRAP_extra1\n",pos);
		exit(1);
		case 18:
		consume_token(map(":="));
		Exp();
		break;
		case 41:
		case 38:
		case 1:
		case 4:
		case 31:
		case 19:
		case 32:
		case 24:
		case 40:
		case 39:
		case 33:
		case 15:
		case 13:
		case 0:
		case 12:
		case 42:
		case 22:
		case 23:
		case 10:
		case 2:
		case 3:
		case 5:
		case 37:
		case 25:
		case 35:
		case 43:
		case 27:
		break;
	}
}
void FunctionRecordArrayPr(){
	//printf("FunctionRecordArrayPr %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d FunctionRecordArrayPr\n",pos);
		exit(1);
		case 41:
		case 18:
		case 38:
		case 1:
		case 4:
		case 31:
		case 36:
		case 19:
		case 32:
		case 24:
		case 40:
		case 39:
		case 33:
		case 15:
		case 13:
		case 0:
		case 12:
		case 42:
		case 22:
		case 23:
		case 10:
		case 2:
		case 3:
		case 5:
		case 37:
		case 25:
		case 34:
		case 35:
		case 43:
		case 27:
		FRAP_extra();
		FRAP_extra1();
		break;
	}
}
void FRAP_extra(){
	//printf("FRAP_extra %s\n",s[pos]);
	switch(map(s[pos])){
		case 41:
		case 18:
		case 38:
		case 1:
		case 4:
		case 31:
		case 19:
		case 32:
		case 24:
		case 40:
		case 39:
		case 33:
		case 15:
		case 13:
		case 0:
		case 12:
		case 42:
		case 22:
		case 23:
		case 10:
		case 2:
		case 3:
		case 5:
		case 37:
		case 25:
		case 35:
		case 43:
		case 27:
		break;
		default:
		printf("Error! pos=%d FRAP_extra\n",pos);
		exit(1);
		case 36:
		consume_token(map("."));
		consume_token(map("id"));
		FRAP_extra();
		break;
		case 34:
		consume_token(map("["));
		Exp();
		consume_token(map("]"));
		FRAP_extra();
		break;
	}
}
void ExpList(){
	//printf("ExpList %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d ExpList\n",pos);
		exit(1);
		case 23:
		case 10:
		break;
		case 9:
		case 8:
		case 20:
		case 7:
		case 14:
		case 17:
		case 11:
		case 16:
		case 3:
		case 6:
		case 21:
		Exp();
		EL_extra();
		break;
	}
}
void EL_extra(){
	//printf("EL_extra %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d EL_extra\n",pos);
		exit(1);
		case 23:
		case 10:
		break;
		case 37:
		consume_token(map(";"));
		Exp();
		EL_extra();
		break;
	}
}
void ArgList(){
	//printf("ArgList %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d ArgList\n",pos);
		exit(1);
		case 10:
		break;
		case 9:
		case 8:
		case 20:
		case 7:
		case 14:
		case 17:
		case 11:
		case 16:
		case 3:
		case 6:
		case 21:
		Exp();
		AL_extra();
		break;
	}
}
void AL_extra(){
	//printf("AL_extra %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d AL_extra\n",pos);
		exit(1);
		case 10:
		break;
		case 31:
		consume_token(map(","));
		Exp();
		AL_extra();
		break;
	}
}
void UnaryOp(){
	//printf("UnaryOp %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d UnaryOp\n",pos);
		exit(1);
		case 3:
		consume_token(map("-"));
		break;
	}
}
void RelationOp(){
	//printf("RelationOp %s\n",s[pos]);
	switch(map(s[pos])){
		default:
		printf("Error! pos=%d RelationOp\n",pos);
		exit(1);
		case 25:
		consume_token(map("="));
		break;
		case 38:
		consume_token(map("!="));
		break;
		case 39:
		consume_token(map(">"));
		break;
		case 40:
		consume_token(map("<"));
		break;
		case 41:
		consume_token(map(">="));
		break;
		case 42:
		consume_token(map("<="));
		break;
	}
}
void pre_process(char s[][10], int* arr, int n)
{
	for (int i = 0; i < n; ++i)
	arr[i] = map(s[i]);
}
int main()
{
	//set string
	char string[30][10] = {"let","type","id","=","array","of","id","var","id",":","id",":=","id","[","integer","]","of","integer","in","id","end", "dol"};
	int n = 21;
	for (int i = 0; i < n+1; ++i)
	{
		int tmp = strlen(string[i]);
		for (int j = 0; j < tmp; ++j)
		{
			s[i][j] = string[i][j];
		}
	}
	
	int arr[n];
	pre_process(string, arr, n);
	pos = 0;
	Prog();
	printf("Parsed Successfully...\n");
	return 0;
}
