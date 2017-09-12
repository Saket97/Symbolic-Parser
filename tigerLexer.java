import java.io.*;
public class tigerLexer implements TigerParserConstants{
	public static void main(String args[]) throws IOException {
		tigerLexer  lexer;
		System.out.println("Reading from file " + args[0] + " . . .");
      try
      {
          lexer = new tigerLexer(new java.io.FileInputStream(args[0]));
          PrintWriter writer = new PrintWriter(args[1], "UTF-8");
          lexer.print(writer);
          writer.close();
      }
      catch (java.io.FileNotFoundException e)
      {
          System.out.println("File " + args[0] + " not found.");
          return;
      }
	}
	
	static public TigerParserTokenManager token_source;
	static JavaCharStream jj_input_stream;
  	/** Current token. */
  	static public Token token;
	static private boolean jj_initialized_once = false;	
	
	public tigerLexer(java.io.Reader stream) {
    	if (jj_initialized_once) {
      		System.out.println("ERROR: Second call to constructor of static parser. ");
      		System.out.println("       You must either use ReInit() or set the JavaCC option STATIC to false");
      		System.out.println("       during parser generation.");
      		throw new Error();
    	}
    	jj_initialized_once = true;
    	jj_input_stream = new JavaCharStream(stream, 1, 1);
    	token_source = new TigerParserTokenManager(jj_input_stream);
    	token = new Token();
    	//jj_ntk = -1;
    	//jj_gen = 0;
    	//for (int i = 0; i < 31; i++) jj_la1[i] = -1;
  	}
  
  	public tigerLexer(java.io.InputStream stream) {
  	   this(stream, null);
  	   System.out.println("Constructor 1");
  	}
  	
  	public tigerLexer(java.io.InputStream stream, String encoding) {
  	  System.out.println("Constructor2");
  	  if (jj_initialized_once) {
  	    System.out.println("ERROR: Second call to constructor of static parser.  ");
  	    System.out.println("       You must either use ReInit() or set the JavaCC option STATIC to false");
  	    System.out.println("       during parser generation.");
  	    throw new Error();
  	  }
  	  jj_initialized_once = true;
  	  try { 
  	  jj_input_stream = new JavaCharStream(stream, encoding, 1, 1); 
  	  } 
  	  catch(java.io.UnsupportedEncodingException e) { throw new RuntimeException(e); }
    	  token_source = new TigerParserTokenManager(jj_input_stream);
    	  token = new Token();
   	// jj_ntk = -1;
   	// jj_gen = 0;
   	// for (int i = 0; i < 31; i++) jj_la1[i] = -1;
  	}


 static public void print(PrintWriter writer){
   int count = 0;
   while(true){
   	Token oldToken;
   	if ((oldToken = token).next != null )token = token.next;
   	else token = token.next = token_source.getNextToken();
   	  if (token.kind == 0){
       return;
     } 
    System.out.println(token.toString());
    System.out.println(token.kind);
    // writer.printf("%s %d %d %d\n",token.toString(),token.beginLine,token.beginColumn,token.endColumn);
    // writer.printf("%s\n",token.toString());
    switch (token.kind)
    {
      case 10:
        writer.printf("array\n");
        break;
      case 11:
        writer.printf("break\n");
        break;
      case 12:
        writer.printf("do\n");
        break;
      case 13:
        writer.printf("else\n");
        break;
      case 14:
        writer.printf("end\n");
        break;
      case 15:
        writer.printf("for\n");
        break;
      case 16:
        writer.printf("function\n");
        break;
      case 17:
        writer.printf("if\n");
        break;
      case 18:
        writer.printf("in\n");
        break;
      case 19:
        writer.printf("let\n");
        break;
      case 20:
        writer.printf("nil\n");
        break;
      case 21:
        writer.printf("of\n");
        break;
      case 22:
        writer.printf("then\n");
        break;
      case 23:
        writer.printf("to\n");
        break;
      case 24:
        writer.printf("type\n");
        break;
      case 25:
        writer.printf("var\n");
        break;
      case 26:
        writer.printf("while\n");
        break;
      case 27:
      writer.printf("+\n");
      break;
      case 28:
        writer.printf("-\n");
        break;
      case 29:
        writer.printf("*\n");
        break;
      case 30:
        writer.printf("/\n");
        break;
      case 31:
        writer.printf("&\n");
        break;
      case 32:
        writer.printf("|\n");
        break;
      case 33:
        writer.printf("=\n");
        break;
      case 34:
        writer.printf("<>\n");
        break;
      case 35:
        writer.printf("<\n");
        break;
      case 36:
        writer.printf("<=\n");
        break;
      case 37:
        writer.printf(">\n");
        break;
      case 38:
        writer.printf(">=\n");
        break;
      case 39:
      writer.printf(":=\n");
      break;
      case 40:
        writer.printf(";\n");
        break;
      case 41:
        writer.printf(",\n");
        break;
      case 42:
        writer.printf(":\n");
        break;
      case 43:
        writer.printf(".\n");
        break;
      case 44:
        writer.printf("(\n");
        break;
      case 45:
        writer.printf(")\n");
        break;
      case 46:
        writer.printf("[\n");
        break;
      case 47:
        writer.printf("]\n");
        break;
      case 48:
        writer.printf("{\n");
        break;
      case 49:
        writer.printf("}\n");
        break;
      case 50:
        writer.printf("id\n");
        break;
      case 51:
        writer.printf("integer\n");
        break;
      case 55:
        writer.printf("string\n");
        break;
      default:
        writer.printf("AAAAA\n");
    }
   	}
   	
   	
   }

}
