public class tigerLexer implements TigerParserConstants{
	public static void main(String args[]){
		tigerLexer  lexer;
		System.out.println("Reading from file " + args[0] + " . . .");
            try
            {
                lexer = new tigerLexer(new java.io.FileInputStream(args[0]));
                lexer.print();
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

  
 static public void print(){
   int count = 0;
   while(true){
   	if (count == 10)
   	return;
   	Token oldToken;
   	if ((oldToken = token).next != null )token = token.next;
   	else token = token.next = token_source.getNextToken();
   	System.out.println(token.toString());
   	System.out.println("token.image "+token.image);
      	/*if (token.next == null)
   	count += 1;*/
   	if (token.kind == 0) return;
   	}
   	
   	
   }

}
