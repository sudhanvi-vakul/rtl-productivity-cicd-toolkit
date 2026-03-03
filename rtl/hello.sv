@'
module hello;
  initial begin
    $display("HELLO_DUT");
  end
endmodule
'@ | Set-Content -NoNewline rtl/hello.sv