@'
module hello_tb;
  hello dut();
  initial begin
    $display("HELLO_TB_START");
    #1;
    $display("HELLO_TB_DONE");
    $finish;
  end
endmodule
'@ | Set-Content -NoNewline tb/hello_tb.sv